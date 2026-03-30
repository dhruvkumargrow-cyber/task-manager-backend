from flask import Flask, request, jsonify
from db import get_connection
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "name": "Task Management REST API",
        "version": "1.0",
        "status": "running",
        "endpoints": {
            "health":  "GET    /health",
            "tasks":   "GET    /tasks",
            "create":  "POST   /tasks",
            "get_one": "GET    /tasks/<id>",
            "update":  "PUT    /tasks/<id>",
            "delete":  "DELETE /tasks/<id>"
        },
        "docs": "github.com/dhruvkumargrow-cyber/task-manager-backend"
    }), 200

# ── GET all tasks ──────────────────────────────────────
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, description, status, created_at, updated_at
        FROM tasks
        ORDER BY created_at DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id":          row[0],
            "title":       row[1],
            "description": row[2],
            "status":      row[3],
            "created_at":  str(row[4]),
            "updated_at":  str(row[5])
        })
    return jsonify(tasks), 200

# ── GET single task ────────────────────────────────────
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, description, status, created_at, updated_at
        FROM tasks WHERE id = %s;
    """, (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id":          row[0],
        "title":       row[1],
        "description": row[2],
        "status":      row[3],
        "created_at":  str(row[4]),
        "updated_at":  str(row[5])
    }), 200

# ── POST create task ───────────────────────────────────
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    title       = data.get('title')
    description = data.get('description', '')
    status      = data.get('status', 'pending')

    if status not in ['pending', 'in_progress', 'completed']:
        return jsonify({"error": "Status must be pending, in_progress or completed"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (title, description, status)
        VALUES (%s, %s, %s)
        RETURNING id, title, description, status, created_at, updated_at;
    """, (title, description, status))
    row = conn.cursor()
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id":          row[0],
        "title":       row[1],
        "description": row[2],
        "status":      row[3],
        "created_at":  str(row[4]),
        "updated_at":  str(row[5])
    }), 201

# ── PUT update task ────────────────────────────────────
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    title       = data.get('title')
    description = data.get('description')
    status      = data.get('status')

    if status and status not in ['pending', 'in_progress', 'completed']:
        return jsonify({"error": "Status must be pending, in_progress or completed"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Check task exists
    cur.execute("SELECT id FROM tasks WHERE id = %s;", (task_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    # Build update query dynamically
    fields = []
    values = []
    if title:
        fields.append("title = %s")
        values.append(title)
    if description is not None:
        fields.append("description = %s")
        values.append(description)
    if status:
        fields.append("status = %s")
        values.append(status)

    fields.append("updated_at = %s")
    values.append(datetime.utcnow())
    values.append(task_id)

    cur.execute(f"""
        UPDATE tasks SET {', '.join(fields)}
        WHERE id = %s
        RETURNING id, title, description, status, created_at, updated_at;
    """, values)

    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id":          row[0],
        "title":       row[1],
        "description": row[2],
        "status":      row[3],
        "created_at":  str(row[4]),
        "updated_at":  str(row[5])
    }), 200

# ── DELETE task ────────────────────────────────────────
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM tasks WHERE id = %s;", (task_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Task deleted successfully"}), 200

# ── Health check ───────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)