from db import get_connection

def get_ideas(query, page, page_size):
    conn = get_connection()
    limit = page_size
    offset = page_size * (page - 1)

    if query:
        ideas = conn.execute("""
            SELECT ideas.id,
                   ideas.title,
                   ideas.description,
                   ideas.filename,
                   ideas.user_id,
                   users.username,
                   COUNT(comments.id) AS comment_count
            FROM ideas
            JOIN users ON ideas.user_id = users.id
            LEFT JOIN comments ON comments.idea_id = ideas.id
            WHERE ideas.title LIKE ? OR ideas.description LIKE ?
            GROUP BY ideas.id
            ORDER BY ideas.id DESC
            LIMIT ? OFFSET ?
        """, ("%" + query + "%", "%" + query + "%", limit, offset)).fetchall()
    else:
        ideas = conn.execute("""
            SELECT ideas.id,
                   ideas.title,
                   ideas.description,
                   ideas.filename,
                   ideas.user_id,
                   users.username,
                   COUNT(comments.id) AS comment_count
            FROM ideas
            JOIN users ON ideas.user_id = users.id
            LEFT JOIN comments ON comments.idea_id = ideas.id
            GROUP BY ideas.id
            ORDER BY ideas.id DESC
            LIMIT ? OFFSET ?
        """, (limit, offset)).fetchall()

    conn.close()
    return ideas

def count_ideas(query):
    conn = get_connection()

    if query:
        count = conn.execute(
            "SELECT COUNT(id) FROM ideas WHERE title LIKE ? OR description LIKE ?",
            ("%" + query + "%", "%" + query + "%")
        ).fetchone()[0]
    else:
        count = conn.execute("SELECT COUNT(id) FROM ideas").fetchone()[0]

    conn.close()
    return count

def add_idea(title, description, filename, user_id, classes):
    conn = get_connection()

    cursor = conn.execute(
        "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
        (title, description, filename, user_id)
    )
    idea_id = cursor.lastrowid

    for class_title, class_value in classes:
        conn.execute(
            "INSERT INTO idea_classes (idea_id, title, value) VALUES (?, ?, ?)",
            (idea_id, class_title, class_value)
        )

    conn.commit()
    conn.close()
    return idea_id

def get_idea(idea_id):
    conn = get_connection()

    idea = conn.execute("""
        SELECT ideas.id,
               ideas.title,
               ideas.description,
               ideas.filename,
               ideas.user_id,
               users.username
        FROM ideas
        JOIN users ON ideas.user_id = users.id
        WHERE ideas.id = ?
    """, (idea_id,)).fetchone()

    conn.close()
    return idea

def update_idea(idea_id, title, description, classes):
    conn = get_connection()

    conn.execute(
        "UPDATE ideas SET title = ?, description = ? WHERE id = ?",
        (title, description, idea_id)
    )

    conn.execute("DELETE FROM idea_classes WHERE idea_id = ?", (idea_id,))
    for class_title, class_value in classes:
        conn.execute(
            "INSERT INTO idea_classes (idea_id, title, value) VALUES (?, ?, ?)",
            (idea_id, class_title, class_value)
        )

    conn.commit()
    conn.close()

def delete_idea(idea_id):
    conn = get_connection()

    conn.execute("DELETE FROM comments WHERE idea_id = ?", (idea_id,))
    conn.execute("DELETE FROM idea_classes WHERE idea_id = ?", (idea_id,))
    conn.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))

    conn.commit()
    conn.close()

def get_all_classes():
    conn = get_connection()

    rows = conn.execute("SELECT title, value FROM classes ORDER BY id").fetchall()

    conn.close()

    classes = {}
    for row in rows:
        if row["title"] not in classes:
            classes[row["title"]] = []
        classes[row["title"]].append(row["value"])
    return classes

def get_classes(idea_id):
    conn = get_connection()

    classes = conn.execute(
        "SELECT title, value FROM idea_classes WHERE idea_id = ? ORDER BY id",
        (idea_id,)
    ).fetchall()

    conn.close()
    return classes

def get_comments(idea_id):
    conn = get_connection()

    comments = conn.execute("""
        SELECT comments.content,
               comments.sent_at,
               comments.user_id,
               users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.idea_id = ?
        ORDER BY comments.id
    """, (idea_id,)).fetchall()

    conn.close()
    return comments

def add_comment(idea_id, user_id, content):
    conn = get_connection()

    conn.execute(
        """INSERT INTO comments (idea_id, user_id, content, sent_at)
           VALUES (?, ?, ?, datetime('now', 'localtime'))""",
        (idea_id, user_id, content)
    )

    conn.commit()
    conn.close()
