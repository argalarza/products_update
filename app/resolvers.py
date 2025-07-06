from ariadne import MutationType
from fastapi import Request
from .models import product_collection
from .jwt_utils import verify_token
from bson.objectid import ObjectId

mutation = MutationType()

@mutation.field("updateProduct")
def resolve_update_product(_, info, id, input):
    request: Request = info.context["request"]
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Falta el token")

    token = auth_header.split(" ")[1]
    user = verify_token(token)

    result = product_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": input}
    )

    if result.matched_count == 0:
        raise Exception("Producto no encontrado")

    return "Producto actualizado correctamente"
