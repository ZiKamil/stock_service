from flask import jsonify
from datetime import datetime
from pydantic import ValidationError
import sys
sys.path.append(".")
from models import Article, CategoryArticle, ArticleSpecification
from app import db
from validate_models import ResponseArticle, ResponseCategory, ResponseSpecification


def api_post_articles(body):
    body = body.dict()
    obj = Article()
    for k, v in body.items():
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    obj_dict = obj.to_dict()
    if body["categories"]:
        categories_list = []
        for i in body['categories']:
            categories_list.append(CategoryArticle(category_id=i, article_id=obj.id))
        db.session.bulk_save_objects(categories_list)
        obj_dict["category"] = categories_list
    if body["specifications"]:
        specifications_list = []
        for i in body['specifications']:
            specifications_list.append(ArticleSpecification(specification_id=i, article_id=obj.id))
        db.session.bulk_save_objects(specifications_list)
        obj_dict["specification"] = specifications_list
    db.session.commit()
    try:
        resp = ResponseArticle(**obj_dict)
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_put_articles(body):
    body = body.dict()
    obj = Article.query.get_or_404(body["id"])
    for k, v in body.items():
        setattr(obj, k, v)
    obj.updated_at = datetime.now()
    obj_dict = obj.to_dict()
    if body["categories"]:
        delete_q = CategoryArticle.__table__.delete().where(CategoryArticle.id.in_(body['categories']))
        db.session.execute(delete_q)
        obj_list = []
        for i in body['categories']:
            obj_list.append(CategoryArticle(category_id=i, article_id=body["id"]))
        db.session.bulk_save_objects(obj_list)
        obj_dict["category"] = obj_list
    if body["specifications"]:
        delete_q = CategoryArticle.__table__.delete().where(ArticleSpecification.id.in_(body['specifications']))
        db.session.execute(delete_q)
        obj_list = []
        for i in body['specifications']:
            obj_list.append(ArticleSpecification(specification_id=i, article_id=body["id"]))
        db.session.bulk_save_objects(obj_list)
        obj_dict["specification"] = obj_list
    db.session.commit()
    try:
        resp = ResponseArticle(**obj_dict)
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp.dict()), 200


def api_delete_articles(body):
    body = body.dict()
    obj = Article.query.get_or_404(body["id"])
    db.session.delete(obj)
    db.session.commit()
    return jsonify({}), 204


def api_get_articles():
    obj_list = Article.query.all()
    resp = []
    try:
        for obj in obj_list:
            resp_art = ResponseArticle(**obj.to_dict())
            resp.append(resp_art.dict())
    except ValidationError as e:
        print(e.json())
        return jsonify({"error": "Failed to serialize response data"}), 500
    return jsonify(resp), 200


def api_get_article(article_id):
    obj = Article.query.get_or_404(article_id)
    cat_art_list = []
    art_spec_list = []
    if obj.category_article:
        for i in obj.category_article:
            cat_art_list.append(ResponseCategory(**i.category.to_dict()).dict())
    if obj.article_specification:
        for i in obj.article_specification:
            art_spec_list.append(ResponseSpecification(**i.specification.to_dict()).dict())
    resp = ResponseArticle(**obj.to_dict(), categories=cat_art_list, specifications=art_spec_list).dict()
    return jsonify(resp), 200