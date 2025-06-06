-- Create the members table for gnS (Genius) member directory
CREATE TABLE IF NOT EXISTS members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    commander_name VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    photo_filename VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on commander_name for faster lookups
CREATE INDEX IF NOT EXISTS idx_members_commander_name ON members(commander_name);

-- Create an index on created_at for ordering
CREATE INDEX IF NOT EXISTS idx_members_created_at ON members(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE members ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations for anonymous users
-- Note: In production, you might want to restrict this further
CREATE POLICY "Allow all operations for anonymous users" ON members
    FOR ALL USING (true);

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
CREATE TRIGGER update_members_updated_at 
    BEFORE UPDATE ON members 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
