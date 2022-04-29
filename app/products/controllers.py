from typing import List

from flask import abort, request
from flask_pydantic import validate
from flask_restx import Namespace, Resource
from pydantic import parse_obj_as

from . import queries
from .models import Product, db
from .schemas import ProductInputSchema, ProductOutputSchema, ProductPatchSchema

api = Namespace("products", path="/api/product")

# create restx special schemas for docs generation
api.schema_model(ProductInputSchema.__name__, ProductInputSchema.schema())
api.schema_model(ProductOutputSchema.__name__, ProductOutputSchema.schema())
api.schema_model(ProductPatchSchema.__name__, ProductPatchSchema.schema())


@api.route("")
class ProductController(Resource):
    model = Product
    in_schema = ProductInputSchema
    out_schema = ProductOutputSchema

    @api.expect(api.models["ProductInputSchema"])
    @api.response(200, "Success", api.models["ProductOutputSchema"])
    @validate()
    def post(self):
        """create new product"""
        data = request.get_json() or {}
        data = self.in_schema(**data)
        product = self.model()

        for name, val in data.dict().items():
            setattr(product, name, val)
        db.session.add(product)
        db.session.commit()

        return self.out_schema.from_orm(product)

    @api.response(200, "Success", api.models["ProductOutputSchema"])
    @validate(response_many=True)
    @api.param("page")
    def get(self):
        """get products list"""
        page = request.args.get("page", 1, type=int)

        items = queries.get_products(page)

        if not items:
            abort(404)

        return parse_obj_as(List[self.out_schema], items)


@api.route("/<string:product_id>")
class ProductDetailController(Resource):
    model = Product
    in_schema = ProductPatchSchema
    out_schema = ProductOutputSchema

    @api.expect(api.models["ProductPatchSchema"])
    @api.response(200, "Success", api.models["ProductOutputSchema"])
    @validate()
    def patch(self, product_id: str):
        """edit product"""
        data = request.get_json() or {}
        data = self.in_schema(**data)
        product = queries.get_product(product_id)

        for name, val in data.dict().items():
            if val is not None:
                setattr(product, name, val)
        db.session.commit()

        return self.out_schema.from_orm(product)

    @api.response(200, "Success", api.models["ProductOutputSchema"])
    @validate()
    def get(self, product_id: str):
        """product details"""
        product = queries.get_product(product_id)
        return self.out_schema.from_orm(product)
