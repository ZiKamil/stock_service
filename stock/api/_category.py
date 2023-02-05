from flask import jsonify
from pydantic import ValidationError
import sys
sys.path.append(".")
from models import Category
from app import db
from validate_models import ResponseCategory, ResponseGroupSpec, ResponseSpecification


def api_post_categories(body):
    obj = Category()
    for k, v in body.dict().items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    try:
        resp = ResponseCategory(**obj.to_dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_put_categories(body):
    body = body.dict()
    obj = Category.query.get_or_404(body["id"])
    for k, v in body.items():
        setattr(obj, k, v)
    db.session.commit()
    try:
        resp = ResponseCategory(**obj.to_dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_delete_categories(body):
    body = body.dict()
    obj = Category.query.get_or_404(body["id"])
    db.session.delete(obj)
    db.session.commit()
    return jsonify({}), 204


def api_get_categories():
    obj_list = Category.query.all()
    resp = []
    try:
        for obj in obj_list:
            resp_cat = ResponseCategory(**obj.to_dict())
            resp.append(resp_cat.dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp), 200


def api_get_category(category_id):
    obj = Category.query.get_or_404(category_id)
    group_list = []
    if obj.group_spec:
        for group in obj.group_spec:
            spec_list = []
            for spec in group.specification:
                spec_list.append(ResponseSpecification(**spec.to_dict()).dict())
            group_list.append(ResponseGroupSpec(**group.to_dict(), specifications=spec_list).dict())
    resp = ResponseCategory(**obj.to_dict(), groupsSpecs=group_list).dict()
    return jsonify(resp), 200
