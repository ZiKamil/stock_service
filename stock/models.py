from datetime import datetime
from flask import Flask, abort, Response
from flask_sqlalchemy import SQLAlchemy, BaseQuery
import json


class CustomBaseQuery(BaseQuery):
    def get_or_404(self, ident, description=None):
        model_class_name = ''
        try:
            model_class_name = self._entity_from_pre_ent_zero().class_.__name__
        except Exception as e:
            print(e)

        rv = self.get(ident)
        if not rv:
            error_message = json.dumps({'error': f'{model_class_name} with id {str(ident)} not found'})
            abort(Response(error_message, 404))
        return rv


db = SQLAlchemy(query_class=CustomBaseQuery)


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(254), nullable=True)
    description = db.Column(db.String(1000), nullable=True)

    category_article = db.relationship("CategoryArticle", back_populates="article")
    article_specification = db.relationship("ArticleSpecification", back_populates="article")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "description": self.description,
        }


class Specification(db.Model):
    __tablename__ = 'specification'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group_spec.id'))
    default_value = db.Column(db.JSON, nullable=True)
    is_required = db.Column(db.Boolean, nullable=False, default_value=False)
    order_namber = db.Column(db.Integer, nullable=False)

    group_spec = db.relationship("GroupSpec", back_populates="specification")
    article_specification = db.relationship("ArticleSpecification", back_populates="specification")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "group_id": self.group_id,
            "default_value": self.default_value,
            "is_required": self.is_required,
            "order_namber": self.order_namber
        }


class GroupSpec(db.Model):
    __tablename__ = 'group_spec'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    category = db.relationship("Category", back_populates="group_spec")
    specification = db.relationship("Specification", back_populates="group_spec")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id
        }


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    group_spec = db.relationship("GroupSpec", back_populates="category")
    category_article = db.relationship("CategoryArticle", back_populates="category")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class CategoryArticle(db.Model):
    __tablename__ = 'category_article'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    category = db.relationship("Category", back_populates="category_article")
    article = db.relationship("Article", back_populates="category_article")


class ArticleSpecification(db.Model):
    __tablename__ = 'article_specification'

    id = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    specification_id = db.Column(db.Integer, db.ForeignKey('specification.id'))
    value = db.Column(db.JSON, nullable=True)

    specification = db.relationship("Specification", back_populates="article_specification")
    article = db.relationship("Article", back_populates="article_specification")
