from fastapi import APIRouter
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.products_model import Products
from fastapi.encoders import jsonable_encoder

router = APIRouter()

class ProductsController:

    def get_products(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT idProduct, NameProduct, Unit FROM Products")
            result = cursor.fetchall()
            payload = []
            for data in result:
                product = {
                    'idProduct': data[0],
                    'NameProduct': data[1],
                    'Unit': data[2]
                }
                payload.append(product)
            return {"resultado": payload}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def get_product_by_id(self, idProduct):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idProduct, NameProduct, Unit FROM products WHERE idProduct = %s", (idProduct,))
            result = cursor.fetchone()
            if result:
                product = {
                    'idProduct': result[0],
                    'NameProduct': result[1],
                    'Unit': result[2]
                }
                return {"resultado": product}
            else:
                return {"resultado": "Producto no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def post_product(self, new_product: Products):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            NameProduct = new_product.NameProduct
            Unit = new_product.Unit
            cursor.execute("INSERT INTO products(NameProduct, Unit) VALUES (%s, %s)",
                           (NameProduct, Unit))
            conn.commit()
            return {"informacion": "Producto registrado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def update_product(self, idProduct: int, new_product: Products):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idProduct FROM products WHERE idProduct = %s", (idProduct,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404, detail="El producto no se encuentra en la base de datos")
            NameProduct = new_product.NameProduct
            Unit = new_product.Unit
            cursor.execute("""
            UPDATE products SET 
            NameProduct = %s,
            Unit = %s
            WHERE idProduct = %s
        """, (NameProduct, Unit, idProduct))
            conn.commit()
            return {"informacion": "Producto actualizado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_product(self, idProduct: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idProduct FROM products WHERE idProduct = %s", (idProduct,))
            result = cursor.fetchone()
            if not result:
                return {"informacion": "El producto no se encuentra en la base de datos"}
            cursor.execute(
                "DELETE FROM products WHERE idProduct = %s", (idProduct,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE products AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Producto eliminado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()


products_controller = ProductsController()
