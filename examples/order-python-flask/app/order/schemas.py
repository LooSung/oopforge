from marshmallow import Schema, fields, validate


class LineSchema(Schema):
    product_id = fields.Str(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Int(required=True, validate=validate.Range(min=0))


class PlaceOrderSchema(Schema):
    customer_id = fields.Str(required=True)
    lines = fields.List(fields.Nested(LineSchema), required=True, validate=validate.Length(min=1))


class OrderResponseSchema(Schema):
    order_id = fields.Str()
