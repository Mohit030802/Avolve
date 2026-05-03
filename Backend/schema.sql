-- Schema for Avolve Backend
-- Database: Avolve

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);
CREATE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE INDEX IF NOT EXISTS ix_users_username ON users (username);

-- Resume Table
CREATE TABLE IF NOT EXISTS resume (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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

-- Career Analysis Table
CREATE TABLE IF NOT EXISTS careeranalysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID NOT NULL REFERENCES resume(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    target_role TEXT NOT NULL,
    duration_weeks INTEGER NOT NULL,
    analysis_data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS ix_careeranalysis_id ON careeranalysis (id);
CREATE INDEX IF NOT EXISTS ix_careeranalysis_resume_id ON careeranalysis (resume_id);
CREATE INDEX IF NOT EXISTS ix_careeranalysis_user_id ON careeranalysis (user_id);

