import psycopg2
from config import HOST, PORT, DBNAME, USER, PASSWORD

conn = psycopg2.connect(
    host=HOST, port=PORT, dbname=DBNAME,
    user=USER, password=PASSWORD, sslmode="require"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id          SERIAL PRIMARY KEY,
        title       VARCHAR(255) NOT NULL,
        description TEXT,
        status      VARCHAR(50)  DEFAULT 'pending',
        created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
        updated_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    );
""")

conn.commit()
cur.close()
conn.close()
print("✅ Tasks table created successfully!")