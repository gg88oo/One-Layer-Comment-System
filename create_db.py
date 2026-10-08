import sqlite3

DB_NAME = "database.db"  # change to match your app

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    text TEXT,
    username TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    comment_text TEXT,
    post_id INTEGER,
    username TEXT
);

CREATE TABLE IF NOT EXISTS sub_comments (
    id INTEGER PRIMARY KEY,
    comment_text TEXT,
    main_comment_id INTEGER,
    reply_to_id INTEGER,  -- NULL = replying to the main comment
    username TEXT
);
"""

def main():
    conn = sqlite3.connect(DB_NAME)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' is ready.")

if __name__ == "__main__":
    main()