-- Database initialisation script (PostgreSQL).
-- Executed automatically by the postgres container on first start.
-- Keep in sync with backend/app/models.py.

CREATE TABLE IF NOT EXISTS projects (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    description VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS activities (
    id                   SERIAL PRIMARY KEY,
    project_id           INTEGER       NOT NULL REFERENCES projects (id) ON DELETE CASCADE,
    name                 VARCHAR(120)  NOT NULL,
    budget_at_completion NUMERIC(14, 2) NOT NULL CHECK (budget_at_completion > 0),
    planned_percent      NUMERIC(5, 2)  NOT NULL CHECK (planned_percent BETWEEN 0 AND 100),
    actual_percent       NUMERIC(5, 2)  NOT NULL CHECK (actual_percent BETWEEN 0 AND 100),
    actual_cost          NUMERIC(14, 2) NOT NULL CHECK (actual_cost >= 0)
);

CREATE INDEX IF NOT EXISTS idx_activities_project_id ON activities (project_id);
