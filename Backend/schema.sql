-- Schema for Avolve Backend
-- Database: Avolve

-- Enable UUID extension if not already present
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Resume Table
CREATE TABLE IF NOT EXISTS resume (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename TEXT NOT NULL,
    raw_markdown TEXT NOT NULL,
    structured_data JSONB NOT NULL DEFAULT '{}',
    user_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS ix_resume_id ON resume (id);
CREATE INDEX IF NOT EXISTS ix_resume_user_id ON resume (user_id);

-- Note: In the future, we will add a VECTOR column here for pgvector support
-- ALTER TABLE resume ADD COLUMN embedding VECTOR(1536); 
