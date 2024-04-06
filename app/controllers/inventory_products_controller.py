from fastapi import APIRouter
import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.inventory_products_model import InventoryProducts
from fastapi.encoders import jsonable_encoder

router = APIRouter()


class InventoryProductsController:

    def get_inventory_products(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, quantity, idInventorySite, idProduct FROM inventory_products")
            result = cursor.fetchall()
            payload = []
            for data in result:
                product = {
                    'id': data[0],
                    'quantity': data[1],
                    'idInventorySite': data[2],
                    'idProduct': data[3]
                }
                payload.append(product)
            return {"resultado": payload}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def get_inventory_product_by_id(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, quantity, idInventorySite, idProduct FROM inventory_products WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                product = {
                    'id': result[0],
                    'quantity': result[1],
                    'idInventorySite': result[2],
                    'idProduct': result[3]
                }
                return {"resultado": product}
            else:
                return {"resultado": "Producto no encontrado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def post_inventory_product(self, new_inventory_product: InventoryProducts):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            quantity = new_inventory_product.quantity
            idInventorySite = new_inventory_product.idInventorySite
            idProduct = new_inventory_product.idProduct
            cursor.execute("INSERT INTO inventory_products(quantity, idInventorySite, idProduct) VALUES (%s, %s, %s)",
                           (quantity, idInventorySite, idProduct))
            conn.commit()
            return {"informacion": "Producto de inventario registrado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def update_inventory_product(self, id: int, new_inventory_product: InventoryProducts):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM inventory_products WHERE id = %s", (id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404, detail="El producto de inventario no se encuentra en la base de datos")
            quantity = new_inventory_product.quantity
            idInventorySite = new_inventory_product.idInventorySite
            idProduct = new_inventory_product.idProduct
            cursor.execute("""
            UPDATE inventory_products SET 
            quantity = %s,
            idInventorySite = %s,
            idProduct = %s
            WHERE id = %s
        """, (quantity, idInventorySite, idProduct, id))
            conn.commit()
            return {"informacion": "Producto de inventario actualizado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_inventory_product(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM inventory_products WHERE id = %s", (id,))
            result = cursor.fetchone()
            if not result:
                return {"informacion": "El producto de inventario no se encuentra en la base de datos"}
            cursor.execute(
                "DELETE FROM inventory_products WHERE id = %s", (id,))
            conn.commit()
            return {"informacion": "Producto de inventario eliminado"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()


inventory_products_controller = InventoryProductsController()
