import sqlite3
from conexion import Conexion
from tabulate import tabulate
class CRUD(Conexion):
    def __init__(self, name_db):
        try:
            super().__init__(name_db)
            self.tabla_seleccionada = None
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def obtener_decision_seguir(self) -> int:
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
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener las tablas: {e}")
            return []

    def imprimir_tablas(self):
        tablas = self.query_gr_tabla()
        if not tablas:
            print("No se encontraron tablas en la base de datos.")
            return

        contador = 0
        for tabla in tablas:
            print(f"{contador}.{''.join(tabla)}")
            contador += 1

    def funtion_selec_table(self):
        while True:
            try:
                selec_table = int(input(f"\n¿Qué tabla desea consultar? "))
                if isinstance(selec_table, int) and 0 <= selec_table < len(self.query_gr_tabla()):
                    self.tabla_seleccionada = selec_table
                    return selec_table
                else:
                    print("Respuesta inválida, inténtalo de nuevo.")
            except ValueError:
                print("La respuesta debe ser un número entero válido.")

    def opcion_crear(self):
        print("\nHas elegido Crear.")
        self.imprimir_tablas()
        select_table = self.funtion_selec_table()

        print("\nINSERTA LOS DATOS CORRESPONDIENTES:")
        nom_empleado = input("\tIngrese el nombre del empleado: ")
        ape_part_empleado = input(f"\tIngrese el apellido paterno de {nom_empleado}: ")
        ape_mart_empleado = input(f"\tIngrese el apellido materno de {nom_empleado}: ")
        edad_empleado = input(f"\tIngrese la edad del empleado: ")
        salario_empleado = int(input(f"\tIngrese el salario: "))

        try:
            self.cursor.execute(f"INSERT INTO {''.join(self.query_gr_tabla()[select_table])}(nombre_empleado, apellido_paterno, apellido_materno, edad, salario) VALUES(?, ?, ?, ?, ?);",
                                (nom_empleado, ape_part_empleado, ape_mart_empleado, edad_empleado, salario_empleado))
            self.conn.commit()
            print(f"Registro insertado.".upper())
        except (sqlite3.Error, ValueError) as e:
            print(f"Error al insertar el registro: {e}")

    def buscar_columna(self):
        select_table = self.funtion_selec_table()
        self.cursor.execute(f"PRAGMA table_info({''.join(self.query_gr_tabla()[select_table])});")
        print("Elija los campos que quiera ver:")
        list_colums = self.cursor.fetchall()
        list_colums.append([len(list_colums), "Todas"])
        for contador, columna in enumerate(list_colums):
            print(f"{contador}.{columna[1]}")

    def selector_columna(self) -> int:
        try:
            select_colum = int(input("\nSegún los índices numéricos.\n¿Qué columnas deseas ver? "))
            return select_colum
        except ValueError:
            print("Respuesta inválida, elija un número válido.")
            return -1

    def opcion_read(self):
        self.imprimir_tablas()
        self.buscar_columna()
        todas_columnas = []
        columnas_consultar = []
        while True:
            self.cursor.execute(f"PRAGMA table_info({''.join(self.query_gr_tabla()[self.tabla_seleccionada])});")
            select_colum = self.selector_columna()
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
                decision_seguir = input("¿Quieres agregar más columnas [Y/N]?")
                if decision_seguir.upper() == "Y":
                    continue
                elif decision_seguir.upper() == "N":
                    break

        query = self.cursor.execute("SELECT " + ", ".join(columnas_consultar) + " FROM " + ''.join(self.query_gr_tabla()[self.tabla_seleccionada]) + ";")

        table = tabulate(query.fetchall(), headers=columnas_consultar, tablefmt="fancy_grid" )
        print(table)

    def opciones(self):
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