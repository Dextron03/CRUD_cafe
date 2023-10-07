import sqlite3
from conexion import Conexion


class CRUD(Conexion):
    def __init__(self, name_db):
        """Inicializa una instancia de la clase CRUD.

        Args:
            name_db (str): El nombre del archivo de base de datos SQLite."""
        super().__init__(name_db)

    def obtener_decision_seguir(self) -> int:
        """Permite al usuario elegir si desea continuar con el proceso o salir del CRUD.
        Returns:
            int: 1 si el usuario desea continuar, 2 si el usuario desea salir."""
        while True:
            try:
                seguir = int(input("\n¿Desea seguir con el proceso?\nPara seguir, digite --> 1\nPara salir, digite --> 2\nIngrese su opción: "))
                if seguir in (1, 2):
                    return seguir
                else:
                    print("Respuesta inválida, inténtalo de nuevo.")
            except ValueError:
                print("La respuesta debe ser un número entero (1 o 2).")

    def query_gr_tabla(self):
        """Retorna la lista de nombres de tablas existentes en la base de datos.

        Returns:
            list: Una lista de nombres de tablas."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()

    def imprimir_tablas(self):
        """Imprime los nombres de las tablas disponibles en la base de datos."""
        tablas = self.query_gr_tabla()
        contador = 0
        for tabla in tablas:
            contador += 1
            print(f"{contador}.{''.join(tabla)}")

    def funtion_selec_table(self):
        """Permite al usuario elegir la tabla con la que quiere trabajar.

        Returns:
            int: El número de la tabla seleccionada."""
        while True:
            try:
                selec_table = int(input(f"\n¿Que tabla desea consultar? "))
                if isinstance(selec_table, int):
                    print(" ")
                    return selec_table
                else:
                    print("Respuesta inválida, inténtalo de nuevo.")
            except ValueError:
                indices = [i for i in range(1, 4)]
                self.imprimir_tablas()
                print(f"Por favor, ingrese el número/índice ({indices}, etc.).")

    def opcion_crear(self):
        """Permite al usuario crear un nuevo registro en la tabla seleccionada."""
        print("\nHas elegido Crear.")
        self.imprimir_tablas()
        select_table = self.funtion_selec_table()

        # Crear/Insertar
        print("\nINSERTA LOS DATOS CORRESPONDIENTES:")
        nom_empleado = input("\tIngrese el nombre del empleado: ")
        ape_part_empleado = input(f"\tIngrese el apellido paterno de {nom_empleado}: ")
        ape_mart_empleado = input(f"\tIngrese el apellido materno de {nom_empleado}: ")
        edad_empleado = input(f"\tIngrese la edad del empleado: ")
        salario_empleado = int(input(f"\tIngrese el salario: "))
        self.cursor.execute(f"INSERT INTO {''.join(self.query_gr_tabla()[0])}(nombre_empleado, apellido_paterno, apellido_materno, edad, salario) VALUES('{nom_empleado}','{ape_part_empleado}','{ape_mart_empleado}','{edad_empleado}', '{salario_empleado}');")
        self.conn.commit()
        print(f"Registro insertado.".upper())
        
    def buscar_columna(self):    
        self.cursor.execute(f"PRAGMA table_info({''.join(self.query_gr_tabla()[0])});")
        print("Que elija los campos que quiera ver:")
        list_colums = self.cursor.fetchall()
        list_colums.append([len(list_colums), "Salir"])  # Agregar "Salir" al final de la lista
        for contador, columna in enumerate(list_colums):
            print(f"{contador}.{columna[1]}")
        
    def opcion_read(self):
        self.imprimir_tablas()
        select_table = self.funtion_selec_table()
        self.buscar_columna()

            
        

        #self.cursor.execute(f"SELECT  FROM {''.join(self.query_gr_tabla()[0])});")

    def opciones(self):
        """Ejecuta el menú principal del CRUD y gestiona las operaciones disponibles."""
        while True:
            try:
                opcion = int(input("\n¿Qué quieres hacer hoy?\n1. Crear\n2. Leer\n3. Actualizar\n4. Eliminar\n5. Salir\n6. Buscar\nDijite su opcion: "))
            except ValueError:
                print("Debes elegir un número válido.")
                continue

            if opcion == 1: #OPCION CREATE
                self.opcion_crear()
                decision_funcion = self.obtener_decision_seguir()
                #self.tomar_decision(decision_funcion)
                if decision_funcion == 1:
                    print("Has elegido seguir.")
                    continue
                elif decision_funcion == 2:
                    print("Has salido del programa.")
                    break
                
            elif opcion == 2: #OPCION LEER
                print("\nHas elegido Leer.".upper())
                self.opcion_read()
                
                decision_funcion = self.obtener_decision_seguir()
                
                if decision_funcion == 1:
                    print("Has elegido seguir.")
                    continue
                elif decision_funcion == 2:
                    print("Has salido del programa.")
                    break
                

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
