import sqlite3

DB_NAME = "logs.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        response_time REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def log_query(question, answer, response_time):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO query_logs
    (
        question,
        answer,
        response_time
    )
    VALUES (?, ?, ?)
    """,
    (
        question,
        answer,
        response_time
    ))

    conn.commit()
    conn.close()

def total_queries():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM query_logs"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def most_frequent_questions():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        question,
        COUNT(*) as frequency
    FROM query_logs
    GROUP BY question
    ORDER BY frequency DESC
    LIMIT 5
    """)

    result = cursor.fetchall()

    conn.close()

    return result

def unanswered_queries():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT question
    FROM query_logs
    WHERE answer LIKE '%I could not find%'
    """)

    result = cursor.fetchall()

    conn.close()

    return result

def average_latency():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(response_time)
    FROM query_logs
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result

