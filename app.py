from flask import Flask, jsonify, request, render_template
import os
import uuid

app = Flask(__name__)
NOTES_DIR = "notes"

# Ensure notes directory exists
os.makedirs(NOTES_DIR, exist_ok=True)


def get_note_path(note_id):
    return os.path.join(NOTES_DIR, f"note_{note_id}.txt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/notes", methods=["POST"])
def create_note():
    """Create a new note"""
    data = request.json
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "Content required"}), 400

    note_id = str(uuid.uuid4())
    with open(get_note_path(note_id), "w") as f:
        f.write(content)

    return jsonify({"id": note_id}), 201


@app.route("/notes", methods=["GET"])
def get_all_notes():
    """List all notes"""
    notes = {}
    for filename in os.listdir(NOTES_DIR):
        if filename.startswith("note_") and filename.endswith(".txt"):
            note_id = filename[5:-4]
            with open(os.path.join(NOTES_DIR, filename), "r") as f:
                notes[note_id] = f.read()
    return jsonify(notes)


@app.route("/notes/<string:note_id>", methods=["GET"])
def get_note(note_id):
    """Get a specific note"""
    if not os.path.exists(get_note_path(note_id)):
        return jsonify({"error": "Note not found"}), 404

    with open(get_note_path(note_id), "r") as f:
        content = f.read()

    return jsonify({"id": note_id, "content": content})


@app.route("/notes/<string:note_id>", methods=["PUT"])
def update_note(note_id):
    """Update an existing note"""
    if not os.path.exists(get_note_path(note_id)):
        return jsonify({"error": "Note not found"}), 404

    data = request.json
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "Content required"}), 400

    with open(get_note_path(note_id), "w") as f:
        f.write(content)

    return jsonify({"id": note_id, "message": "Note updated"})


@app.route("/notes/<string:note_id>", methods=["DELETE"])
def delete_note(note_id):
    """Delete a note"""
    if not os.path.exists(get_note_path(note_id)):
        return jsonify({"error": "Note not found"}), 404

    os.remove(get_note_path(note_id))
    return jsonify({"message": "Note deleted"})


@app.route("/health")
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
