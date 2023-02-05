from app import app, db
from flask import request
from flask_pydantic import validate
from validate_models import *
from api._category import *
from api._group_spec import *
from api._specification import *
from api._articles import *


@app.route('/categories', methods=['POST'])
@validate()
def post_categories(body: PostCategoryModel):
    return api_post_categories(body)


@app.route('/categories', methods=['PUT'])
@validate()
def put_categories(body: PutCategoryModel):
    return api_put_categories(body)


@app.route('/categories', methods=['DELETE'])
@validate()
def delete_categories(body: DeleteCategoryModel):
    return api_delete_categories(body)


@app.route('/categories', methods=['GET'])
def get_categories():
    return api_get_categories()


@app.route('/categories/<int:category_id>', methods=['GET'])
@validate()
def get_category(category_id: int):
    return api_get_category(category_id)


@app.route('/group_specs', methods=['POST'])
@validate()
def post_group_specs(body: PostGroupSpecModel):
    return api_post_group_specs(body)


@app.route('/group_specs', methods=["PUT"])
@validate()
def put_group_specs(body: PutCategoryModel):
    return api_put_group_specs(body)


@app.route('/group_specs', methods=["DELETE"])
@validate()
def delete_group_specs(body: DeleteGroupSpecModel):
    return api_delete_group_specs(body)


@app.route('/group_specs', methods=['GET'])
def get_group_specs():
    return api_get_group_specs()


@app.route('/group_specs/<int:gs_id>', methods=['GET'])
@validate()
def get_group_spec(gs_id: int):
    return api_get_group_spec(gs_id)


@app.route('/specifications', methods=['POST'])
@validate()
def specifications(body: PostSpecificationModel):
    return api_post_specifications(body)


@app.route('/specifications', methods=["PUT"])
@validate()
def put_specifications(body: PutSpecificationModel):
    return api_put_specifications(body)


@app.route('/specifications', methods=["DELETE"])
@validate()
def delete_specifications(body: DeleteSpecificationModel):
    return api_delete_specifications(body)


@app.route('/specifications', methods=['GET'])
def get_specifications():
    return api_get_specifications()


@app.route('/specifications/<int:spec_id>', methods=['GET'])
@validate()
def get_specification(spec_id: int):
    return api_get_specification(spec_id)


@app.route('/articles', methods=['POST'])
@validate()
def post_articles(body: PostArticleModel):
    return api_post_articles(body)


@app.route('/articles', methods=["PUT"])
@validate()
def put_articles(body: PutArticleModel):
    return api_put_articles(body)


@app.route('/articles', methods=["DELETE"])
@validate()
def delete_articles(body: DeleteArticleModel):
    return api_delete_articles(body)


@app.route('/articles', methods=['GET'])
def get_articles():
    return api_get_articles()


@app.route('/articles/<int:article_id>', methods=['GET'])
@validate()
def get_article(article_id: int):
    return api_get_article(article_id)
