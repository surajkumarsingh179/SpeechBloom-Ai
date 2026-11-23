-- ==============================================================
-- SpeechBloom AI - Supabase Database & Storage Setup Schema
-- Run this in your Supabase SQL Editor (https://supabase.com/dashboard)
-- ==============================================================

-- 1. Create Profiles Table (extends Supabase Auth Users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'parent' CHECK (role IN ('parent', 'therapist', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Create Child Profiles Table
CREATE TABLE IF NOT EXISTS public.child_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    name TEXT NOT NULL,
    age INTEGER CHECK (age >= 1 AND age <= 18),
    languages JSONB DEFAULT '["english"]'::jsonb,
    avatar TEXT DEFAULT '🧒',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Create Audio Recordings Table
CREATE TABLE IF NOT EXISTS public.recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID REFERENCES public.child_profiles(id) ON DELETE CASCADE NOT NULL,
    audio_url TEXT NOT NULL,
    language TEXT NOT NULL,
    target_word TEXT,
    target_phoneme TEXT,
    observed_transcript TEXT,
    duration NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Create Practice Sessions Table
CREATE TABLE IF NOT EXISTS public.practice_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID REFERENCES public.child_profiles(id) ON DELETE CASCADE NOT NULL,
    recording_id UUID REFERENCES public.recordings(id) ON DELETE SET NULL,
    recording_url TEXT,
    target_word TEXT,
    target_phoneme TEXT,
    observed_phoneme TEXT,
    score NUMERIC NOT NULL,
    feedback TEXT,
    error_category TEXT DEFAULT 'none',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Create Badges Table
CREATE TABLE IF NOT EXISTS public.badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    child_id UUID REFERENCES public.child_profiles(id) ON DELETE CASCADE NOT NULL,
    badge_type TEXT NOT NULL,
    badge_name TEXT NOT NULL,
    earned_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 6. Enable Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.child_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recordings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.practice_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.badges ENABLE ROW LEVEL SECURITY;

-- 7. RLS Policies
-- Profiles: Users can view and edit their own profile
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

-- Child Profiles: Parents can only access their own children
CREATE POLICY "Parents can view their children"
    ON public.child_profiles FOR SELECT
    USING (auth.uid() = parent_id);

CREATE POLICY "Parents can insert their children"
    ON public.child_profiles FOR INSERT
    WITH CHECK (auth.uid() = parent_id);

CREATE POLICY "Parents can update their children"
    ON public.child_profiles FOR UPDATE
    USING (auth.uid() = parent_id);

CREATE POLICY "Parents can delete their children"
    ON public.child_profiles FOR DELETE
    USING (auth.uid() = parent_id);

-- Practice Sessions: Parents can view practice history of their children
CREATE POLICY "Parents can view practice sessions of their children"
    ON public.practice_sessions FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.child_profiles
            WHERE public.child_profiles.id = public.practice_sessions.child_id
            AND public.child_profiles.parent_id = auth.uid()
        )
    );

-- 8. Storage Bucket for Audio Recordings
-- Create 'speech-recordings' bucket if not already created
INSERT INTO storage.buckets (id, name, public)
VALUES ('speech-recordings', 'speech-recordings', true)
ON CONFLICT (id) DO NOTHING;

-- Storage Policy: Allow authenticated users to upload speech audio
CREATE POLICY "Allow authenticated audio uploads"
    ON storage.objects FOR INSERT
    WITH CHECK (bucket_id = 'speech-recordings');

CREATE POLICY "Allow public read of speech audio"
    ON storage.objects FOR SELECT
    USING (bucket_id = 'speech-recordings');
