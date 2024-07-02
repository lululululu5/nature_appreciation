import sqlite3
from flask import Flask, request, jsonify, abort, g

app = Flask(__name__)
DATABASE = "sustainability_tips.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This allows us to access columns by name
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    if exception:
        print(f"An exception occurred: {exception}")


@app.route("/tips", methods=["GET", "POST"])
def handle_tips():
    if request.method == "POST":
        if not request.json or not "title" in request.json:
            abort(400, description="Missing title")
        if not "content" in request.json:
            abort(400, description="Missing content")

        title = request.json.get("title")
        content = request.json.get("content")
        category = request.json.get("category", "General")
        author = request.json.get("author", "mapache")

        try:
            query_db("""
                     INSERT INTO tips (title, content, category, author)
                     VALUES (?, ?, ?, ?)
                     """, (title, content, category, author))

            get_db().commit()

            return jsonify({"status": "Tip added successfully"}), 201

        except sqlite3.Error as e:
            get_db().rollback()
            abort(500, description="Database error: {}".format(str(e)))

    elif request.method == "GET":
        tips = query_db("SELECT * FROM tips")

        tips_list = []
        for tip in tips:
            tips_list.append({
                "id": tip["id"],
                "title": tip["title"],
                "content": tip["content"],
                "category": tip["category"],
                "author": tip["author"],
                "date_added": tip["date_added"]
            })

        return jsonify(tips_list)


@app.route("/delete_tip/<int:id>", methods=["DELETE"])
def delete_tip(id):
    tip = query_db("SELECT * FROM tips WHERE id = ?", [id], one=True)
    if tip is None:
        return jsonify({"error": "Tip not found"}), 404

    query_db("DELETE FROM tips WHERE id = ?", [id])

    get_db().commit()

    return jsonify({"status": "Tip deleted successfully"}), 200
