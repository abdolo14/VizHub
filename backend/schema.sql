-- Repositories table
CREATE TABLE IF NOT EXISTS repositories (
    id SERIAL PRIMARY KEY,
    github_id INTEGER UNIQUE,
    name VARCHAR(255),
    owner VARCHAR(255),
    stars INTEGER,
    forks INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Contributors table
CREATE TABLE IF NOT EXISTS contributors (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    github_username VARCHAR(255),
    contributions INTEGER,
    UNIQUE(repository_id, github_username)
);

-- Commit activity table
CREATE TABLE IF NOT EXISTS commit_activity (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    week TIMESTAMP,
    total_commits INTEGER,
    UNIQUE(repository_id, week)
);

-- Language distribution table
CREATE TABLE IF NOT EXISTS language_distribution (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    language VARCHAR(100),
    bytes INTEGER,
    UNIQUE(repository_id, language)
);

-- Issues table
CREATE TABLE IF NOT EXISTS issues (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id),
    github_issue_id INTEGER,
    title VARCHAR(255),
    state VARCHAR(50),
    created_at TIMESTAMP,
    closed_at TIMESTAMP,
    UNIQUE(repository_id, github_issue_id)
);
