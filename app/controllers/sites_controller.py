import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.sites_model import Sites
from fastapi.encoders import jsonable_encoder


class SitesController:

    def get_sites(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Sites")
            result = cursor.fetchall()
            payload = []
            content = {}
            for data in result:
                content = {
                    'Name': data[1],
                    'Address': data[2]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        except Exception as error:
            return {"resultado": str(error)}

    def get_sites_id(self, idSite):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sites WHERE idSite = %s", (idSite,))
            result = cursor.fetchone()
            if result:
                Site = {
                    'Name': result[1],
                    'Address': result[2]
                }
                return {"resultado": Site}
            else:
                return {"resultado": "Sede no encontrada"}
        except Exception as error:
            return {"resultado": str(error)}

    def post_sites(self, newsites: Sites):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            Name = newsites.Name
            Address = newsites.Address
            cursor.execute("INSERT INTO sites(Name,Address) VALUES (%s,%s)",
                           (Name, Address))
            conn.commit()
            conn.close()
            return {"informacion": "Nueva Sede Registrada"}
        except Exception as error:
            return {"resultado": str(error)}

    def update_sites(self, idSite: int, newsites: Sites):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idSite FROM sites WHERE idSite = %s", (idSite,))
            resultado = cursor.fetchone()
            if not resultado:
                raise HTTPException(
                    status_code=404, detail="La sede no se encuentra en la base de datos")
            Name = newsites.Name
            Address = newsites.Address
            cursor.execute("""
            UPDATE sites SET 
            Name = %s,
            Address = %s
            WHERE idSite = %s
        """, (Name, Address, idSite))
            conn.commit()
            return {"informacion": "Sede actualizada"}
        except Exception as error:
            return {"resultado": str(error)}
        finally:
            cursor.close()
            conn.close()

    def delete_sites(self, idSite: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idSite FROM Sites WHERE idSite = %s", (idSite,))
            resultado = cursor.fetchone()
            if not resultado:
                return {"informacion": "La sede no se encuentra en la base de datos"}
            cursor.execute(
                "DELETE FROM Sites WHERE idSite = %s", (idSite,))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE Sites AUTO_INCREMENT = 1")
            conn.commit()
            return {"informacion": "Sede eliminada"}
        except Exception as error:
            return {"resultado": str(error)}


sites_controller = SitesController()
