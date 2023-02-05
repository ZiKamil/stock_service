from flask import jsonify
from pydantic import ValidationError
import sys
sys.path.append(".")
from models import Specification
from app import db
from validate_models import ResponseSpecification


def api_post_specifications(body):
    obj = Specification()
    for k, v in body.dict().items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    try:
        resp = ResponseSpecification(**obj.to_dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_put_specifications(body):
    body = body.dict()
    obj = Specification.query.get_or_404(body["id"])
    for k, v in body.items():
        setattr(obj, k, v)
    db.session.commit()
    try:
        resp = ResponseSpecification(**obj.to_dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_delete_specifications(body):
    body = body.dict()
    obj = Specification.query.get_or_404(body["id"])
    db.session.delete(obj)
    db.session.commit()
    return jsonify({}), 204


def api_get_specifications():
    obj_list = Specification.query.all()
    resp = []
    try:
        for obj in obj_list:
            resp_spec = ResponseSpecification(**obj.to_dict())
            resp.append(resp_spec.dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp), 200


def api_get_specification(spec_id):
    obj = Specification.query.get_or_404(spec_id)
    resp = ResponseSpecification(**obj.to_dict()).dict()
    return jsonify(resp), 200
