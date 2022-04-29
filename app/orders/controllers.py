from flask import request
from flask_pydantic import validate
from flask_restx import Namespace, Resource

from app.products import queries as product_queries

from . import queries
from .models import OrderProduct, db
from .schemas import AddProductSchema, OrderSchema

api = Namespace("orders", path="/api/order")

# create restx special schemas for docs generation
api.schema_model(AddProductSchema.__name__, AddProductSchema.schema())
api.schema_model(OrderSchema.__name__, OrderSchema.schema())


@api.route("")
class OrderController(Resource):
    in_schema = AddProductSchema
    out_schema = OrderSchema

    @api.expect(api.models["AddProductSchema"])
    @api.response(200, "Success", api.models["OrderSchema"])
    @validate()
    def post(self):
        """add/delete product to order"""
        data = request.get_json() or {}
        data = self.in_schema(**data)
        order = queries.get_current_order()
        product = product_queries.get_product(data.product_id)
        order_product = queries.get_product_from_order(order, product)

        # if count = 0 - remove product
        if data.count == 0:
            if order_product:
                # remove product
                db.session.delete(order_product)
        else:
            if not order_product:
                # create new order_product
                order_product = OrderProduct()
                order_product.product = product
            order_product.count = data.count
            order.products.append(order_product)

        db.session.commit()

        return self.out_schema.from_orm(order)

    @api.response(200, "Success", api.models["OrderSchema"])
    @validate()
    def get(self):
        """get current order (cart)"""
        order = queries.get_current_order()
        return self.out_schema.from_orm(order)
