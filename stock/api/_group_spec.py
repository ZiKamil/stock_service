from flask import jsonify
from pydantic import ValidationError
import sys
sys.path.append(".")
from models import GroupSpec
from app import db
from validate_models import ResponseGroupSpec, ResponseSpecification


def api_post_group_specs(body):
    obj = GroupSpec()
    for k, v in body.dict().items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    try:
        resp = ResponseGroupSpec(**obj.to_dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_put_group_specs(body):
    body = body.dict()
    obj = GroupSpec.query.get_or_404(body["id"])
    for k, v in body.items():
        setattr(obj, k, v)
    db.session.commit()
    try:
        resp = ResponseGroupSpec(**obj.to_dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_delete_group_specs(body):
    body = body.dict()
    obj = GroupSpec.query.get_or_404(body["id"])
    db.session.delete(obj)
    db.session.commit()
    return jsonify({}), 204


def api_get_group_specs():
    obj_list = GroupSpec.query.all()
    resp = []
    try:
        for obj in obj_list:
            resp_group = ResponseGroupSpec(**obj.to_dict())
            resp.append(resp_group.dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp), 200


def api_get_group_spec(gs_id):
    obj = GroupSpec.query.get_or_404(gs_id)
    obj_list = []
    if obj.specification:
        for i in obj.specification:
            obj_list.append(ResponseSpecification(**i.to_dict()).dict())
    resp = ResponseGroupSpec(**obj.to_dict(), specifications=obj_list).dict()
    return jsonify(resp), 200