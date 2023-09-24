import sqlite3

class Conxion:
    def __init__(self,name_db : str):
        self.name_db = name_db
    
    def conexion(self):
        try:
            conn = sqlite3.connect(self.name_db)
            cursor = conn.cursor()
            print("Conexion exitosa.")
        except sqlite3.Error as e:
            # Si se produce un error al conectarse, muestra un mensaje de error
            print(f"Error al conectar a la base de datos: {e}")
            
        cursor.close()
        conn.close()

class CRUD(Conxion):
    def __init__(self, name_db: str):
        super().__init__(name_db)
        
    def opciones(self):
        """Este metodo esta hecho con el fin de poder hacer un menu para las acciones del CRUD."""
        select_op : list = ["CREAR","LEER","ACTUALIZAR","ELIMINAR","SALIR","SEGUIR"]
        select_op_num = [i for i in range(1,7,1)] #Genera una lista de numeros automaticamente.
        for op,num_op in zip(select_op,select_op_num): #Recorrer a la par las 2 listas.
            print(f"{num_op}.{op}")
    
    
db_conex = CRUD('./intento_CRUD/empleados.db')
db_conex.conexion()
db_conex.opciones()