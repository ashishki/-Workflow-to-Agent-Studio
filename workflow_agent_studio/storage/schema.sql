PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS workflow_runs (
    run_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    schema_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_documents (
    source_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    title TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    normalized_text TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES workflow_runs(run_id),
    UNIQUE (run_id, fingerprint)
);

CREATE TABLE IF NOT EXISTS blueprint_versions (
    blueprint_version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    version_number INTEGER NOT NULL,
    blueprint_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES workflow_runs(run_id),
    UNIQUE (run_id, version_number)
);

CREATE TABLE IF NOT EXISTS blueprint_approvals (
    blueprint_version_id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL,
    reviewer_label TEXT NOT NULL,
    approved_at TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (blueprint_version_id) REFERENCES blueprint_versions(blueprint_version_id),
    FOREIGN KEY (run_id) REFERENCES workflow_runs(run_id)
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES workflow_runs(run_id)
);
