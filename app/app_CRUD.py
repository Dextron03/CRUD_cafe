import sqlite3

class Conexion:
    def __init__(self, name_db):
        self.name_db = name_db
        self.conn = None  # Mantén la conexión como un atributo de la instancia

    def abrir_conexion(self):
        try:
            self.conn = sqlite3.connect(self.name_db)
            self.cursor = self.conn.cursor()
            print("Conexion exitosa.")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            print("Conexion cerrada.")

class CRUD(Conexion):
    def __init__(self, name_db):
        super().__init__(name_db)

    def opciones(self):
        while True:
            try:
                opcion = int(input("\n¿Qué quieres hacer hoy?\n1. Crear\n2. Leer\n3. Actualizar\n4. Eliminar\n5. Salir\n6. Seguir\nDijite su opcion: "))
            except ValueError:
                print("Debes elegir un número válido.")
                continue

            if opcion == 1:
                print("\nHas elegido Crear.")
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                query = self.cursor.fetchall()
                
                contador = 0
                for tablas in query:
                    contador = contador + 1
                    print(f"{contador}.{''.join(tablas)}")
                
                selec_table : str = int(input(f"¿A que base de datos desea insertarle datos? "))
                if selec_table == 1:
                    nom_empleado : str = input("Ingrese el nombre del empleado: ")
                    ape_part_empleado : str = input(f"Ingrese el apellido_paterno de {nom_empleado}: ")
                    ape_mart_empleado : str = input(f"Ingrese el apellido_materno de {nom_empleado}: ")
                    edad_empleado : str = input(f"Ingrese la edad del empleado: ")
                    self.cursor.execute(f"INSERT INTO "+"".join(query[0])+f"(nombre_empleado, apellido_paterno, apellido_materno, edad) VALUES('{nom_empleado}','{ape_part_empleado}','{ape_mart_empleado}','{edad_empleado}');")
                    self.conn.commit()
                break    
            elif opcion == 2:
                print("Has elegido Leer.")
                
            elif opcion == 3:
                print("Has elegido Actualizar.")
                
            elif opcion == 4:
                print("Has elegido Eliminar.")
                
            elif opcion == 5:
                print("Saliendo del programa.")
                self.cerrar_conexion()  # Cierra la conexión antes de salir
                break
            elif opcion == 6:
                print("Siguiendo con el programa.")
            else:
                print("Opción no válida. Por favor, elige una opción válida.")

if __name__ == "__main__":
    db_conex = CRUD('./db/cafe.db')
    db_conex.abrir_conexion()
    db_conex.opciones()
