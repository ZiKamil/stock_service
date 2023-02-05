import datetime

from pydantic import BaseModel
from flask import Flask, request
from typing import Optional, TypedDict


class DefaultValue(TypedDict):
    name: str
    type: str
    group_id: int
    is_required: bool
    order_namber: int


class PostCategoryModel(BaseModel):
    name: str
    description: Optional[str]


class PutCategoryModel(BaseModel):
    id: int
    name: str
    description: Optional[str]


class DeleteCategoryModel(BaseModel):
    id: int


class ResponseCategory(BaseModel):
    id: int
    name: str
    description: Optional[str]
    groupsSpecs: Optional[list]


class PostGroupSpecModel(BaseModel):
    category_id: int
    name: str
    description: Optional[str]


class PutGroupSpecModel(BaseModel):
    id: int
    category_id: int
    name: str
    description: Optional[str]


class DeleteGroupSpecModel(BaseModel):
    id: int


class ResponseGroupSpec(BaseModel):
    id: int
    category_id: int
    name: str
    description: Optional[str]
    specifications: Optional[list]


class PostSpecificationModel(BaseModel):
    name: str
    type: str
    group_id: int
    default_value: Optional[DefaultValue]
    is_required: bool
    order_namber: int


class PutSpecificationModel(BaseModel):
    id: int
    name: str
    type: str
    group_id: int
    default_value: Optional[DefaultValue]
    is_required: bool
    order_namber: int


class DeleteSpecificationModel(BaseModel):
    id: int


class ResponseSpecification(BaseModel):
    id: int
    name: str
    type: str
    group_id: int
    default_value: Optional[DefaultValue]
    is_required: bool
    order_namber: int


class PostArticleModel(BaseModel):
    name: str
    full_name: Optional[str]
    description: Optional[str]
    specifications: Optional[list]
    categories: Optional[list]


class PutArticleModel(BaseModel):
    id: int
    name: str
    full_name: Optional[str]
    description: Optional[str]
    specifications: Optional[list]
    categories: Optional[list]


class DeleteArticleModel(BaseModel):
    id: int


class ResponseArticle(BaseModel):
    id: int
    name: str
    full_name: Optional[str]
    description: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    specifications: Optional[list]
    categories: Optional[list]
