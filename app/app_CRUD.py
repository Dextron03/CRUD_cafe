import sqlite3
from conexion import Conexion
from tabulate import tabulate

class CRUD(Conexion):
    def __init__(self, nombre_db):
        """
        Inicializa una instancia de la clase CRUD.

        Parámetros:
        nombre_db (str): Nombre del archivo de la base de datos.

        Atributos:
        tabla_seleccionada (int): Almacena el índice de la tabla seleccionada por el usuario.
        """
        try:
            super().__init__(nombre_db)
            self.tabla_seleccionada = None
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def obtener_decision_seguir(self) -> int:
        """
        Permite al usuario decidir si desea seguir con el proceso o salir.

        Retorna:
        int: La decisión del usuario (1 para seguir, 2 para salir).
        """
        while True:
            try:
                seguir = int(input("\n¿Desea seguir con el proceso?\nPara seguir, digite --> 1\nPara salir, digite --> 2\nIngrese su opción: "))
                if seguir in (1, 2):
                    return seguir
                else:
                    print("Respuesta inválida, inténtalo de nuevo.")
            except ValueError:
                print("La respuesta debe ser un número entero (1 o 2).")

    def consulta_tablas(self):
        """
        Recupera el nombre de todas las tablas en la base de datos.

        Retorna:
        list: Una lista de nombres de tablas en la base de datos.
        """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener las tablas: {e}")
            return []

    def imprimir_tablas(self):
        """
        Imprime los nombres de las tablas en la base de datos.
        """
        tablas = self.consulta_tablas()
        if not tablas:
            print("No se encontraron tablas en la base de datos.")
            return

        contador = 0
        for tabla in tablas:
            print(f"{contador}.{''.join(tabla)}")
            contador += 1

    def seleccionar_tabla(self):
        """
        Permite al usuario seleccionar una tabla de la base de datos.

        Retorna:
        int: El índice de la tabla seleccionada por el usuario.
        """
        while True:
            try:
                selec_table = int(input(f"\n¿Qué tabla desea consultar? "))
                if isinstance(selec_table, int) and 0 <= selec_table < len(self.consulta_tablas()):
                    self.tabla_seleccionada = selec_table
                    return selec_table
                else:
                    print("Respuesta inválida, inténtalo de nuevo.")
            except ValueError:
                print("La respuesta debe ser un número entero válido.")

    def opcion_crear(self):
        """
        Opción para crear un registro en la tabla seleccionada por el usuario.
        """
        print("\nHas elegido Crear.")
        self.imprimir_tablas()
        select_table = self.seleccionar_tabla()

        print("\nINSERTA LOS DATOS CORRESPONDIENTES:")
        nom_empleado = input("\tIngrese el nombre del empleado: ")
        ape_part_empleado = input(f"\tIngrese el apellido paterno de {nom_empleado}: ")
        ape_mart_empleado = input(f"\tIngrese el apellido materno de {nom_empleado}: ")
        edad_empleado = input(f"\tIngrese la edad del empleado: ")
        salario_empleado = int(input(f"\tIngrese el salario: "))

        try:
            columns = self.cursor.execute(f"PRAGMA table_info({''.join(self.consulta_tablas()[select_table])});")
            lista_columnas = columns.fetchall()
            
            self.cursor.execute(f"INSERT INTO {''.join(self.consulta_tablas()[select_table])}(nombre_empleado, apellido_paterno, apellido_materno, edad, salario) VALUES(?, ?, ?, ?, ?);",
                                (nom_empleado, ape_part_empleado, ape_mart_empleado, edad_empleado, salario_empleado))
            self.conn.commit()
            print(f"Registro insertado.".upper())
        except (sqlite3.Error, ValueError) as e:
            print(f"Error al insertar el registro: {e}")

    def buscar_columna(self):
        """
        Permite al usuario elegir las columnas a consultar en la tabla seleccionada.
        """
        select_table = self.seleccionar_tabla()
        self.cursor.execute(f"PRAGMA table_info({''.join(self.consulta_tablas()[select_table])});")
        print("Elija los campos que quiera ver:")
        list_colums = self.cursor.fetchall()
        list_colums.append([len(list_colums), "Todas"])
        for contador, columna in enumerate(list_colums):
            print(f"{contador}.{columna[1]}")

    def seleccionar_columna(self) -> int:
        """
        Permite al usuario seleccionar una columna específica para mostrar.

        Retorna:
        int: El índice de la columna seleccionada.
        """
        try:
            select_colum = int(input("\nSegún los índices numéricos.\n¿Qué columnas deseas ver? "))
            return select_colum
        except ValueError:
            print("Respuesta inválida, elija un número válido.")
            return -1

    def opcion_leer(self):
        """
        Opción para consultar registros en la tabla seleccionada.
        """
        self.imprimir_tablas()
        self.buscar_columna()
        todas_columnas = []
        columnas_consultar = []
        while True:
            self.cursor.execute(f"PRAGMA table_info({''.join(self.consulta_tablas()[self.tabla_seleccionada])});")
            select_colum = self.seleccionar_columna()
            columnas_tablas: list = self.cursor.fetchall()

            while len(columnas_tablas) > len(todas_columnas):
                for i in columnas_tablas:
                    todas_columnas.append(i[1])

            if select_colum == 6:
                columnas_consultar = todas_columnas[:]
            elif 0 <= select_colum < len(columnas_tablas):
                columnas_consultar.append(todas_columnas[select_colum])
            else:
                print("Respuesta inválida, elija un índice válido.")
                continue

            if select_colum == 6:
                break
            else:
                decision_seguir = input("¿Quieres agregar más columnas [S/N]?")
                if decision_seguir.upper() == "S":
                    continue
                elif decision_seguir.upper() == "N":
                    break

        query = self.cursor.execute("SELECT " + ", ".join(columnas_consultar) + " FROM " + ''.join(self.consulta_tablas()[self.tabla_seleccionada]) + ";")
        
        headers = columnas_consultar[:]
        tabla : tabulate = tabulate(query.fetchall(), headers=headers, tablefmt="fancy_grid")
        print(tabla)

    def opciones(self):
        """
        Menú de opciones para el usuario, que incluye Crear, Leer, Actualizar, Eliminar, Buscar y Salir.
        """
        while True:
            try:
                opcion = int(input("\n¿Qué quieres hacer hoy?\n1. Crear\n2. Leer\n3. Actualizar\n4. Eliminar\n5. Salir\n6. Buscar\nDijite su opción: "))
            except ValueError:
                print("Debes elegir un número válido.")
                continue

            if opcion == 1:
                self.opcion_crear()
                decision_funcion = self.obtener_decision_seguir()
                if decision_funcion == 1:
                    print("Has elegido seguir.")
                    continue
                elif decision_funcion == 2:
                    print("Has salido del programa.")
                    break

            elif opcion == 2:
                print("\nHas elegido Leer.".upper())
                self.opcion_leer()

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
                self.cerrar_conexion()
                break
            elif opcion == 6:
                print("Siguiendo con el programa.")
            else:
                print("Opción no válida. Por favor, elige una opción válida.")

if __name__ == "__main__":
    try:
        db_conex = CRUD('./db/cafe.db')
        db_conex.abrir_conexion()
        db_conex.opciones()
    except sqlite3.Error as e:
        print(f"Error al iniciar la aplicación: {e}")
