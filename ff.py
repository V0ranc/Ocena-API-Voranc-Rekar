import sqlite3

DB_pot="db2.sqlite3"
conn = sqlite3.connect(DB_pot)
c = conn.cursor()

c.execute("DELETE FROM user")
c.execute("DELETE FROM post")
c.execute("DELETE FROM com")

c.execute("DELETE FROM sqlite_sequence")  # reset ID

conn.commit()
conn.close()