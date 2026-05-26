from flask import Blueprint, jsonify, request

from app.database import db
from app.models import Comment


bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok, third test"})


@bp.get("/comments")
def list_comments():
    comments = Comment.query.order_by(Comment.created_at.asc()).all()
    return jsonify([comment.to_dict() for comment in comments])


@bp.post("/comments")
def create_comment():
    payload = request.get_json(silent=True) or {}
    author = _clean_required_string(payload.get("author"))
    content = _clean_required_string(payload.get("content"))

    errors = {}
    if author is None:
        errors["author"] = "author is required and cannot be blank"
    if content is None:
        errors["content"] = "content is required and cannot be blank"

    if errors:
        return jsonify({"errors": errors}), 400

    comment = Comment(author=author, content=content)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


def _clean_required_string(value) -> str | None:
    if not isinstance(value, str):
        return None

    cleaned = value.strip()
    if not cleaned:
        return None

    return cleaned
