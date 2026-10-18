import db

def get_ideas(query, page, page_size):
    limit = page_size
    offset = page_size * (page - 1)

    if query:
        sql = """SELECT ideas.id,
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
                 LIMIT ? OFFSET ?"""
        like = "%" + query + "%"
        return db.query(sql, [like, like, limit, offset])

    sql = """SELECT ideas.id,
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
             LIMIT ? OFFSET ?"""
    return db.query(sql, [limit, offset])

def count_ideas(query):
    if query:
        sql = "SELECT COUNT(id) FROM ideas WHERE title LIKE ? OR description LIKE ?"
        like = "%" + query + "%"
        return db.query(sql, [like, like])[0][0]

    sql = "SELECT COUNT(id) FROM ideas"
    return db.query(sql)[0][0]

def add_idea(title, description, filename, user_id, class_ids):
    sql = "INSERT INTO ideas (title, description, filename, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, filename, user_id])
    idea_id = db.last_insert_id()

    sql = "INSERT INTO idea_classes (idea_id, class_id) VALUES (?, ?)"
    for class_id in class_ids:
        db.execute(sql, [idea_id, class_id])

    return idea_id

def get_idea(idea_id):
    sql = """SELECT ideas.id,
                    ideas.title,
                    ideas.description,
                    ideas.filename,
                    ideas.user_id,
                    users.username
             FROM ideas
             JOIN users ON ideas.user_id = users.id
             WHERE ideas.id = ?"""
    result = db.query(sql, [idea_id])
    return result[0] if result else None

def update_idea(idea_id, title, description, class_ids):
    sql = "UPDATE ideas SET title = ?, description = ? WHERE id = ?"
    db.execute(sql, [title, description, idea_id])

    sql = "DELETE FROM idea_classes WHERE idea_id = ?"
    db.execute(sql, [idea_id])

    sql = "INSERT INTO idea_classes (idea_id, class_id) VALUES (?, ?)"
    for class_id in class_ids:
        db.execute(sql, [idea_id, class_id])

def delete_idea(idea_id):
    sql = "DELETE FROM comments WHERE idea_id = ?"
    db.execute(sql, [idea_id])
    sql = "DELETE FROM idea_classes WHERE idea_id = ?"
    db.execute(sql, [idea_id])
    sql = "DELETE FROM ideas WHERE id = ?"
    db.execute(sql, [idea_id])

def get_all_classes():
    sql = "SELECT id, title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for row in result:
        if row["title"] not in classes:
            classes[row["title"]] = []
        classes[row["title"]].append(row)
    return classes

def get_classes(idea_id):
    sql = """SELECT classes.title,
                    GROUP_CONCAT(classes.value, ', ') AS class_values
             FROM idea_classes
             JOIN classes ON idea_classes.class_id = classes.id
             WHERE idea_classes.idea_id = ?
             GROUP BY classes.title
             ORDER BY MIN(classes.id)"""
    return db.query(sql, [idea_id])

def get_class_ids(idea_id):
    sql = "SELECT class_id FROM idea_classes WHERE idea_id = ?"
    result = db.query(sql, [idea_id])

    class_ids = []
    for row in result:
        class_ids.append(row["class_id"])
    return class_ids

def get_comments(idea_id):
    sql = """SELECT comments.content,
                    comments.sent_at,
                    comments.user_id,
                    users.username
             FROM comments
             JOIN users ON comments.user_id = users.id
             WHERE comments.idea_id = ?
             ORDER BY comments.id"""
    return db.query(sql, [idea_id])

def add_comment(idea_id, user_id, content):
    sql = """INSERT INTO comments (idea_id, user_id, content, sent_at)
             VALUES (?, ?, ?, datetime('now', 'localtime'))"""
    db.execute(sql, [idea_id, user_id, content])
