import sqlite3
from app_CRUD import CRUD

if __name__ == "__main__":
    try:
        db_conex = CRUD('./db/cafe.db')
        db_conex.abrir_conexion()
        db_conex.opciones()
    except sqlite3.Error as e:
        print(f"Error al iniciar la aplicación: {e}")