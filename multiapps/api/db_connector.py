import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    database="VAS_DB",
    user="postgres",
    password="gZg4cSRWngqvGxf"
)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())

cur.close()
conn.close()
