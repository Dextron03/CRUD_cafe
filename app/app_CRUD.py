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
                print("Has elegido Crear.")
                query = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                for tablas in query:
                    contador =+ 1
                    print(f"\n{contador}.{''.join(tablas)}")
                
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
