from fastapi import APIRouter, HTTPException
from models.products_model import Products
from controllers.products_controller import ProductsController

router = APIRouter()
products_controller = ProductsController()


@router.get("/products", response_model=dict)
async def get_products():
    return products_controller.get_products()


@router.get("/products/{idProduct}", response_model=dict)
async def get_product_by_id(idProduct: int):
    return products_controller.get_product_by_id(idProduct)


@router.post("/products", response_model=dict)
async def post_product(new_product: Products):
    return products_controller.post_product(new_product)


@router.put("/products/{idProduct}", response_model=dict)
async def update_product(idProduct: int, new_product: Products):
    return products_controller.update_product(idProduct, new_product)


@router.delete("/products/{idProduct}", response_model=dict)
async def delete_product(idProduct: int):
    return products_controller.delete_product(idProduct)
