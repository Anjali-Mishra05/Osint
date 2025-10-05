import sqlite3

def create_table(db_path, table_name="social_media_posts"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            user TEXT,
            timestamp TEXT,
            text TEXT,
            url TEXT,
            sentiment TEXT
        )
    """)
    conn.commit()
    conn.close()


def check_duplicate(db_path, table_name, record):
    """
    Check if a record already exists in the database.
    We'll consider it duplicate if platform + user + text are same.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"""
        SELECT 1 FROM {table_name} 
        WHERE platform=? AND user=? AND text=?
        LIMIT 1
    """, (record["platform"], record["user"], record["text"]))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def save_to_db(records, db_path, table_name="social_media_posts"):
    """
    Save multiple records to database, skip duplicates automatically.
    """
    create_table(db_path, table_name)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    inserted = 0
    for rec in records:
        if not check_duplicate(db_path, table_name, rec):
            c.execute(f"""
                INSERT INTO {table_name} (platform, user, timestamp, text, url, sentiment)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                rec["platform"],
                rec["user"],
                rec["timestamp"],
                rec["text"],
                rec["url"],
                rec["sentiment"]
            ))
            inserted += 1
    conn.commit()
    conn.close()
    return inserted
