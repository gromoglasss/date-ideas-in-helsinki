from db import get_connection

def get_ideas(query=None):
    conn = get_connection()

    if query:
        ideas = conn.execute("""
            SELECT ideas.id,
                   ideas.title,
                   ideas.description,
                   ideas.filename,
                   ideas.user_id,
                   users.username
            FROM ideas
            JOIN users ON ideas.user_id = users.id
            WHERE ideas.title LIKE ? OR ideas.description LIKE ?
            ORDER BY ideas.id DESC
        """, ("%" + query + "%", "%" + query + "%")).fetchall()
    else:
        ideas = conn.execute("""
            SELECT ideas.id,
                   ideas.title,
                   ideas.description,
                   ideas.filename,
                   ideas.user_id,
                   users.username
            FROM ideas
            JOIN users ON ideas.user_id = users.id
            ORDER BY ideas.id DESC
        """).fetchall()

    conn.close()
    return ideas

def add_idea(title, description, filename, user_id):
    conn = get_connection()

    conn.execute(
        "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)",
        (title, description, filename, user_id)
    )

    conn.commit()
    conn.close()

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

def update_idea(idea_id, title, description):
    conn = get_connection()

    conn.execute(
        "UPDATE ideas SET title = ?, description = ? WHERE id = ?",
        (title, description, idea_id)
    )

    conn.commit()
    conn.close()

def delete_idea(idea_id):
    conn = get_connection()

    conn.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))

    conn.commit()
    conn.close()