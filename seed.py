# Fills the database with a large amount of test data.
# NOTE: this deletes all existing users, ideas and comments.
import random
import sqlite3
import config

USER_COUNT = 1000
IDEA_COUNT = 10**5
COMMENT_COUNT = 10**6

answer = input("Tämä poistaa kaikki tiedot tiedostosta " + config.database_file
               + ". Jatketaanko? (k/e) ")
if answer != "k":
    raise SystemExit

conn = sqlite3.connect(config.database_file)

with open("schema.sql", encoding="utf-8") as f:
    conn.executescript(f.read())

conn.execute("DELETE FROM comments")
conn.execute("DELETE FROM idea_classes")
conn.execute("DELETE FROM ideas")
conn.execute("DELETE FROM users")

for i in range(1, USER_COUNT + 1):
    conn.execute("INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)",
                 (i, "user" + str(i), ""))

for i in range(1, IDEA_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    conn.execute("""INSERT INTO ideas (id, title, description, filename, user_id)
                    VALUES (?, ?, ?, ?, ?)""",
                 (i, "idea" + str(i), "kuvaus " + str(i), "", user_id))

for i in range(1, COMMENT_COUNT + 1):
    idea_id = random.randint(1, IDEA_COUNT)
    user_id = random.randint(1, USER_COUNT)
    conn.execute("""INSERT INTO comments (idea_id, user_id, content, sent_at)
                    VALUES (?, ?, ?, datetime('now'))""",
                 (idea_id, user_id, "kommentti " + str(i)))

conn.commit()
conn.close()
