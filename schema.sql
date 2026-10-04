CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    filename TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    value TEXT
);

CREATE TABLE IF NOT EXISTS idea_classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER REFERENCES ideas,
    title TEXT,
    value TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idea_id INTEGER REFERENCES ideas,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_comments_idea ON comments (idea_id);
CREATE INDEX IF NOT EXISTS idx_ideas_user ON ideas (user_id);
CREATE INDEX IF NOT EXISTS idx_idea_classes_idea ON idea_classes (idea_id);
CREATE INDEX IF NOT EXISTS idx_comments_user ON comments (user_id);
