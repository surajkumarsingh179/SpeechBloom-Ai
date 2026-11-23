# 🌸 SpeechBloom AI
**Multilingual AI-Powered Speech Therapy & Pronunciation Practice Platform for Children**

SpeechBloom AI is built according to the modern cloud architecture:
```
               ┌────────────────────────────────────────────────────────┐
               │                        Frontend                        │
               │                  HTML, CSS, JavaScript                 │
               │            Parent / Child / Therapist Dashboard        │
               └───────────────────────────┬────────────────────────────┘
                                           │
                                           ▼
               ┌────────────────────────────────────────────────────────┐
               │                     Django Backend                     │
               │   Authentication integration, APIs, permissions, logic │
               └─────────────────────┬────────────────────┬─────────────┘
                                     │                    │
                                     ▼                    ▼
               ┌───────────────────────────┐    ┌───────────────────────────┐
               │         Supabase          │    │         AI Engine         │
               │ PostgreSQL, Auth, Storage │    │  Speech Analysis, ML,     │
               │                           │    │  Phonetic Alignment       │
               └───────────────────────────┘    └───────────────────────────┘
```

---

## 👨‍👩‍👧 Complete Parent & Child Workflow

1. **Parent Account Registration**:
   - The parent visits `/register/` and signs up with their name, email, and password.
   - Authentication is managed securely via **Supabase Auth** (with local database fallback).

2. **Add Child Profile**:
   - Once signed up, the parent is immediately redirected to `/profile/` to create their child's learner profile (Name, Age, Language preferences like Hindi and English, and an Avatar).
   - The child's profile is saved into Supabase's `child_profiles` PostgreSQL table.

3. **Daily Speech Practice Activities**:
   - The child practices phonemes and words at `/practice/`, `/recording/`, or through **6 interactive speech games** (`/games/`).
   - The in-browser audio recorder encodes directly to standard 16kHz PCM `.wav` with real-time speech captions.
   - The audio recording is securely uploaded to **Supabase Storage** (`speech-recordings` bucket).
   - The **AI Engine** runs acoustic and phonetic evaluation, identifying clean articulations vs sound substitutions (e.g., detecting if the child said *"lun"* instead of *"sun"*).

4. **Parent Monitoring & Detailed Reports**:
   - The parent navigates to `/parent/` to monitor:
     - Total practice sessions and minutes practiced.
     - Average pronunciation accuracy.
     - **Phoneme Articulation Breakdown**: Visual bar charts of *Clear Articulations*, *Sound Substitutions*, and *Sound Distortions*.
     - **Daily Activity History**: Detailed session records showing date, score, observed articulation, and SLP notes.
     - **Printable Clinical Report**: One-click printable summary for pediatricians and Speech-Language Pathologists.

---

## ⚡ Quick Supabase Setup (Optional Cloud Mode)

The system runs in **hybrid mode** — it works out-of-the-box locally, and seamlessly connects to your Supabase project as soon as credentials are added!

1. Create a free project at [supabase.com](https://supabase.com).
2. Go to the **SQL Editor** in your Supabase dashboard and run the script in:
   ```
   database/supabase_schema.sql
   ```
   *(This creates the `profiles`, `child_profiles`, `practice_sessions`, and `recordings` tables, configures Row Level Security, and creates the `speech-recordings` storage bucket).*
3. Copy your Supabase Project URL and Anon/Service-Role Key into your `.env` file:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-supabase-anon-or-service-role-key
   ```

---

## 🚀 How to Run the Application (Windows / VS Code)

### Step 1: Open Terminal in Project Directory
```powershell
cd "c:\Users\HP\OneDrive\Desktop\project_wrk\SpeechBloom-AI"
```

### Step 2: Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Run Database Migrations
```powershell
python manage.py migrate
```

### Step 4: Start the Django Server
```powershell
python manage.py runserver 8000
```

### Step 5: Open in Your Browser
Open your browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🔑 Pre-seeded Demo Credentials
- **Email:** `demo@speechbloom.ai`
- **Password:** `demo1234`
- **Learners:** Pre-seeded with profiles for **Aarav** (Age 6, Hindi + English) and **Ananya** (Age 5, English + Hindi).

---

## 🧪 Automated Test Verification
Run Django's complete test suite:
```powershell
python manage.py test core
```
*(All 3 test suites covering Parent signup, Child creation, Daily practice logging, Detailed reports, and Phonetic evaluation pass).*
