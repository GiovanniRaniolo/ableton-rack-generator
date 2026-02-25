-- 0. Cleanup (Run this to ensure a clean state if you had errors previously)
DROP TABLE IF EXISTS public.collection_items CASCADE;
DROP TABLE IF EXISTS public.collections CASCADE;

-- 1. Collections Table
CREATE TABLE IF NOT EXISTS public.collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL, -- Clerk ID
    name TEXT NOT NULL,
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Collection Items Table (Many-to-Many Link)
CREATE TABLE IF NOT EXISTS public.collection_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id UUID NOT NULL REFERENCES public.collections(id) ON DELETE CASCADE,
    generation_id UUID NOT NULL REFERENCES public.generations(id) ON DELETE CASCADE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(collection_id, generation_id)
);

-- Enable RLS
ALTER TABLE public.collections ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.collection_items ENABLE ROW LEVEL SECURITY;

-- Policies for Collections
CREATE POLICY "Users can view their own collections" 
ON public.collections FOR SELECT 
USING (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub');

CREATE POLICY "Users can create their own collections" 
ON public.collections FOR INSERT 
WITH CHECK (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub');

CREATE POLICY "Users can update their own collections" 
ON public.collections FOR UPDATE 
USING (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub');

CREATE POLICY "Users can delete their own collections" 
ON public.collections FOR DELETE 
USING (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub');

-- Policies for Collection Items
-- Note: We check ownership via the parent collection
CREATE POLICY "Users can view items in their collections" 
ON public.collection_items FOR SELECT 
USING (EXISTS (
    SELECT 1 FROM public.collections 
    WHERE id = collection_id AND (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub')
));

CREATE POLICY "Users can add items to their collections" 
ON public.collection_items FOR INSERT 
WITH CHECK (EXISTS (
    SELECT 1 FROM public.collections 
    WHERE id = collection_id AND (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub')
));

CREATE POLICY "Users can remove items from their collections" 
ON public.collection_items FOR DELETE 
USING (EXISTS (
    SELECT 1 FROM public.collections 
    WHERE id = collection_id AND (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub')
));

CREATE POLICY "Users can update items in their collections" 
ON public.collection_items FOR UPDATE 
USING (EXISTS (
    SELECT 1 FROM public.collections 
    WHERE id = collection_id AND (user_id = auth.uid()::text OR user_id = current_setting('request.jwt.claims', true)::json->>'sub')
));

-- Function to ensure every user has a default "Favorites" collection
CREATE OR REPLACE FUNCTION public.ensure_favorites_exists()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.collections (user_id, name, is_favorite)
    VALUES (NEW.id, 'Favorites', TRUE)
    ON CONFLICT DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create Favorites on profile creation (assuming profiles table exists and handles user registration)
-- If the trigger is already handled by another process, this is a safety fallback.
-- CREATE TRIGGER on_profile_created_favorites
--     AFTER INSERT ON public.profiles
--     FOR EACH ROW EXECUTE FUNCTION public.ensure_favorites_exists();
