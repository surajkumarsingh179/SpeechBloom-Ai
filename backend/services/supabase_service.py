"""
SpeechBloom AI - Supabase Service
Handles Supabase Authentication, PostgreSQL Database operations, and Storage for audio recordings.
Includes resilient fallback when Supabase keys are in demo/local mode.
"""
import os
import json
from datetime import datetime

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False


class SupabaseService:
    """Service wrapping Supabase Auth, Database (PostgreSQL), and Object Storage."""

    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL", "").strip()
        # Clean URL in case user pasted with trailing /rest/v1 or /
        if self.url:
            self.url = self.url.rstrip('/')
            if self.url.endswith('/rest/v1'):
                self.url = self.url[:-8].rstrip('/')

        self.key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY", "").strip()
        self.service_role_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        self.client: Client = None
        self.is_connected = False

        if SUPABASE_AVAILABLE and self.url and self.key:
            try:
                # Use service role key if available for server-side management, otherwise anon key
                active_key = self.service_role_key if self.service_role_key else self.key
                self.client = create_client(self.url, active_key)
                self.is_connected = True
                print(f"[SupabaseService] Connected to Supabase at {self.url}")
            except Exception as e:
                print(f"[SupabaseService] Supabase connection error: {e}")
                self.is_connected = False
        else:
            print("[SupabaseService] Supabase credentials not set or incomplete. Running in hybrid local mode.")

    # -------------------------------------------------------------
    # AUTHENTICATION
    # -------------------------------------------------------------
    def sign_up_parent(self, email, password, name, role='parent'):
        """Register a new parent or therapist account via Supabase Auth."""
        if self.is_connected and self.client:
            try:
                res = self.client.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "name": name,
                            "role": role
                        }
                    }
                })
                user = res.user
                if user:
                    # Also insert/upsert into public.profiles table
                    profile_data = {
                        "id": user.id,
                        "email": email,
                        "name": name,
                        "role": role,
                        "created_at": datetime.utcnow().isoformat()
                    }
                    try:
                        self.client.table("profiles").upsert(profile_data).execute()
                    except Exception as e:
                        print(f"[SupabaseService] Notice upserting profile: {e}")

                    return {
                        "success": True,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "name": name,
                            "role": role
                        },
                        "session": res.session
                    }
            except Exception as e:
                return {"success": False, "message": str(e)}

        return None  # Fallback to local DB

    def sign_in_parent(self, email, password):
        """Sign in a parent or therapist with email and password via Supabase."""
        if self.is_connected and self.client:
            try:
                res = self.client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                if res.user:
                    # Fetch profile metadata
                    profile = {}
                    try:
                        p_res = self.client.table("profiles").select("*").eq("id", res.user.id).execute()
                        if p_res.data:
                            profile = p_res.data[0]
                    except Exception:
                        pass

                    return {
                        "success": True,
                        "user": {
                            "id": res.user.id,
                            "email": res.user.email,
                            "name": profile.get("name", res.user.user_metadata.get("name", email.split('@')[0])),
                            "role": profile.get("role", res.user.user_metadata.get("role", "parent"))
                        },
                        "access_token": res.session.access_token if res.session else None
                    }
            except Exception as e:
                return {"success": False, "message": str(e)}

        return None

    # -------------------------------------------------------------
    # CHILD PROFILES
    # -------------------------------------------------------------
    def create_child_profile(self, parent_id, name, age, languages, avatar="🧒"):
        """Save a new child profile to Supabase 'child_profiles' table."""
        if self.is_connected and self.client:
            try:
                data = {
                    "parent_id": str(parent_id),
                    "name": name,
                    "age": int(age),
                    "languages": languages if isinstance(languages, list) else json.loads(languages),
                    "avatar": avatar,
                    "created_at": datetime.utcnow().isoformat()
                }
                res = self.client.table("child_profiles").insert(data).execute()
                if res.data:
                    return {"success": True, "child": res.data[0]}
            except Exception as e:
                print(f"[SupabaseService] Child profile insert error: {e}")
                return {"success": False, "message": str(e)}

        return None

    def get_children_for_parent(self, parent_id):
        """Fetch all children linked to a parent from Supabase."""
        if self.is_connected and self.client:
            try:
                res = self.client.table("child_profiles").select("*").eq("parent_id", str(parent_id)).execute()
                return res.data or []
            except Exception as e:
                print(f"[SupabaseService] Fetch children error: {e}")
                return []
        return None

    # -------------------------------------------------------------
    # STORAGE: AUDIO RECORDINGS
    # -------------------------------------------------------------
    def upload_recording_audio(self, file_bytes, filename, content_type="audio/wav", bucket_name="speech-recordings"):
        """
        Upload audio recording bytes to Supabase Storage bucket.
        Returns the public or signed URL of the uploaded recording.
        """
        if self.is_connected and self.client:
            try:
                # Ensure bucket exists
                try:
                    self.client.storage.get_bucket(bucket_name)
                except Exception:
                    try:
                        self.client.storage.create_bucket(bucket_name, options={"public": True})
                    except Exception:
                        pass

                # Upload file
                res = self.client.storage.from_(bucket_name).upload(
                    path=filename,
                    file=file_bytes,
                    file_options={"content-type": content_type, "upsert": "true"}
                )

                # Get public URL
                public_url = self.client.storage.from_(bucket_name).get_public_url(filename)
                return public_url
            except Exception as e:
                print(f"[SupabaseService] Storage upload error: {e}")
                return None
        return None

    # -------------------------------------------------------------
    # PRACTICE SESSIONS & PROGRESS
    # -------------------------------------------------------------
    def log_practice_session(self, child_id, recording_url, target_word, target_phoneme, observed_phoneme, score, feedback, error_category):
        """Record a completed practice session into Supabase 'practice_sessions' table."""
        if self.is_connected and self.client:
            try:
                session_data = {
                    "child_id": str(child_id),
                    "recording_url": recording_url or "",
                    "target_word": target_word,
                    "target_phoneme": target_phoneme,
                    "observed_phoneme": observed_phoneme,
                    "score": float(score),
                    "feedback": feedback,
                    "error_category": error_category,
                    "created_at": datetime.utcnow().isoformat()
                }
                res = self.client.table("practice_sessions").insert(session_data).execute()
                return res.data[0] if res.data else None
            except Exception as e:
                print(f"[SupabaseService] Practice session insert error: {e}")
                return None
        return None

    def get_child_practice_history(self, child_id, limit=50):
        """Fetch historical practice records for a child from Supabase."""
        if self.is_connected and self.client:
            try:
                res = self.client.table("practice_sessions").select("*")\
                    .eq("child_id", str(child_id))\
                    .order("created_at", desc=True)\
                    .limit(limit).execute()
                return res.data or []
            except Exception as e:
                print(f"[SupabaseService] Get practice history error: {e}")
                return []
        return None


# Global singleton instance
supabase_service = SupabaseService()
