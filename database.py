import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
id INTEGER PRIMARY KEY,
nome TEXT,
saldo REAL DEFAULT 0,
pix TEXT DEFAULT '',
convidados INTEGER DEFAULT 0,
convidado_por INTEGER DEFAULT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS saques(
id INTEGER PRIMARY KEY AUTOINCREMENT,
usuario INTEGER,
valor REAL,
status TEXT
)
""")

conn.commit()
