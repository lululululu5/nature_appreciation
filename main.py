import sqlite3
import random
from flask import Flask, request, jsonify, abort, g
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config['DATABASE'] = 'sustainability_tips.db'
auth = HTTPBasicAuth()


# Example for admin authentication.
users = {"admin": "password123"}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
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


@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None


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
@auth.login_required
def delete_tip(id):
    tip = query_db("SELECT * FROM tips WHERE id = ?", [id], one=True)
    if tip is None:
        return jsonify({"error": "Tip not found"}), 404

    query_db("DELETE FROM tips WHERE id = ?", [id])

    get_db().commit()

    return jsonify({"status": "Tip deleted successfully"}), 200


@app.route("/search")
def search_tip():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    wildcard_query = f"%{query}%"
    search_results = query_db("""SELECT * FROM tips
            WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
            """, [wildcard_query, wildcard_query, wildcard_query])

    tips_list = []
    for tip in search_results:
        tips_list.append({
            "id": tip["id"],
            "title": tip["title"],
            "content": tip["content"],
            "category": tip["category"],
            "author": tip["author"],
            "date_added": tip["date_added"]
        })

    return jsonify(tips_list), 200


@app.route("/random_tip", methods=["GET"])
def random_tip():
    size = query_db("SELECT COUNT(*) FROM tips", one=True)[0]
    if size == 0:
        return jsonify({"error": "No tips available"}), 404

    i = random.randint(1, size)

    tip = None
    while not tip:
        tip = query_db("SELECT * FROM tips WHERE id = ?", [i], one=True)
        if not tip:
            i = random.randint(1, size)

    return jsonify({
        "id": tip["id"],
        "title": tip["title"],
        "content": tip["content"],
        "category": tip["category"],
        "author": tip["author"],
        "date_added": tip["date_added"]}), 200
