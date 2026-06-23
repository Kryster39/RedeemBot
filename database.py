import sqlite3

DB_NAME = "bot.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS codes (
        code TEXT PRIMARY KEY
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_viewed (
        user_id TEXT,
        code TEXT,
        PRIMARY KEY (user_id, code)
    )
    """)

    conn.commit()
    conn.close()


# ---------- codes ----------

def add_codes(codes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    new_codes = []
    for code in codes:
        try:
            c.execute("INSERT INTO codes (code) VALUES (?)", (code,))
            new_codes.append(code)
        except:
            pass

    conn.commit()
    conn.close()
    return new_codes


def get_all_codes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT code FROM codes")
    rows = [r[0] for r in c.fetchall()]

    conn.close()
    return rows


# ---------- user view ----------

def mark_viewed(user_id, codes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for code in codes:
        c.execute("""
        INSERT OR IGNORE INTO user_viewed (user_id, code)
        VALUES (?, ?)
        """, (user_id, code))

    conn.commit()
    conn.close()


def get_viewed(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT code FROM user_viewed
    WHERE user_id=?
    """, (user_id,))

    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return rows


def get_unviewed(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT code FROM codes
    WHERE code NOT IN (
        SELECT code FROM user_viewed WHERE user_id=?
    )
    """, (user_id,))

    rows = [r[0] for r in c.fetchall()]
    conn.close()
    return rows