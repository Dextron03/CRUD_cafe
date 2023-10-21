import sqlite3
from conexion import Conexion
from tabulate import tabulate

class CRUD(Conexion):
    def __init__(self, nombre_db):
        try:
            super().__init__(nombre_db)
            self.tabla_seleccionada = None  # Variable para almacenar la tabla seleccionada
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def obtener_decision_seguir(self) -> int:
        """Obtiene la decisión del usuario de continuar o salir del proceso."""
        while True:
            try:
                eleccion = int(input("\n¿Desea continuar con el proceso?\nPara continuar, escriba --> 1\nPara salir, escriba --> 2\nIngrese su elección: "))
                if eleccion in (1, 2):
                    return eleccion
                else:
                    print("Respuesta inválida, inténtelo de nuevo.")
            except ValueError:
                print("La respuesta debe ser un número entero (1 o 2).")

    def obtener_nombres_tablas(self):
        """Obtiene los nombres de las tablas en la base de datos."""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener las tablas: {e}")
            return []

    def mostrar_tablas(self):
        """Muestra las tablas disponibles en la base de datos."""
        tablas = self.obtener_nombres_tablas()
        if not tablas:
            print("No se encontraron tablas en la base de datos.")
            return

        contador = 0
        for tabla in tablas:
            print(f"{contador}.{''.join(tabla)}")
            contador += 1

    def seleccionar_tabla(self):
        """Permite al usuario seleccionar una tabla para operar."""
        while True:
            try:
                tabla_seleccionada = int(input(f"\n¿Qué tabla desea consultar? "))
                if isinstance(tabla_seleccionada, int) and 0 <= tabla_seleccionada < len(self.obtener_nombres_tablas()):
                    self.tabla_seleccionada = tabla_seleccionada
                    return tabla_seleccionada
                else:
                    print("Respuesta inválida, inténtelo de nuevo.")
            except ValueError:
                print("La respuesta debe ser un número entero válido.")

    def opcion_crear_registro(self):
        """Permite al usuario insertar un nuevo registro en la tabla seleccionada."""
        print("\nHas elegido Crear.")
        self.mostrar_tablas()
        tabla_seleccionada = self.seleccionar_tabla()

        print("\nINSERTA LOS DATOS CORRESPONDIENTES:")
        nombre_empleado = input("\tIngrese el nombre del empleado: ")
        apellido_paterno_empleado = input(f"\tIngrese el apellido paterno de {nombre_empleado}: ")
        apellido_materno_empleado = input(f"\tIngrese el apellido materno de {nombre_empleado}: ")
        edad_empleado = input(f"\tIngrese la edad del empleado: ")
        salario_empleado = int(input(f"\tIngrese el salario: "))

        try:
            # Crea un nuevo registro en la tabla seleccionada con los datos proporcionados
            self.cursor.execute(f"INSERT INTO {''.join(self.obtener_nombres_tablas()[tabla_seleccionada])}(nombre_empleado, apellido_paterno, apellido_materno, edad, salario) VALUES(?, ?, ?, ?, ?);",
                                (nombre_empleado, apellido_paterno_empleado, apellido_materno_empleado, edad_empleado, salario_empleado))
            self.conn.commit()  # Guarda los cambios en la base de datos
            print(f"Registro insertado.".upper())
        except (sqlite3.Error, ValueError) as e:
            print(f"Error al insertar el registro: {e}")
    
    def mostrar_columnas(self):
        """Permite al usuario seleccionar las columnas a mostrar."""
        self.cursor.execute(f"PRAGMA table_info({''.join(self.obtener_nombres_tablas()[self.tabla_seleccionada])});")
        print("Elige las columnas que deseas ver:")
        lista_columnas = self.cursor.fetchall()
        lista_columnas.append([len(lista_columnas), "Todas"])
        for contador, columna in enumerate(lista_columnas):
            print(f"{contador}.{columna[1]}")

    def seleccionar_columna(self) -> int:
        """Permite al usuario seleccionar una columna específica para mostrar."""
        try:
            columna_seleccionada = int(input("\nSegún los índices numéricos.\n¿Qué columnas deseas ver? "))
            return columna_seleccionada
        except ValueError:
            print("Respuesta inválida, elija un número válido.")
            return -1

    def opcion_leer(self):
        """Permite al usuario consultar registros de la tabla seleccionada."""
        self.mostrar_tablas()
        self.mostrar_columnas()
        todas_columnas = []
        columnas_a_consultar = []
        while True:
            self.cursor.execute(f"PRAGMA table_info({''.join(self.obtener_nombres_tablas()[self.tabla_seleccionada])});")
            columna_seleccionada = self.seleccionar_columna()
            columnas_tabla: list = self.cursor.fetchall()

            while len(columnas_tabla) > len(todas_columnas):
                for i in columnas_tabla:
                    todas_columnas.append(i[1])

            if columna_seleccionada == 6:
                columnas_a_consultar = todas_columnas[:]
            elif 0 <= columna_seleccionada < len(columnas_tabla):
                columnas_a_consultar.append(todas_columnas[columna_seleccionada])
            else:
                print("Respuesta inválida, elija un índice válido.")
                continue

            if columna_seleccionada == 6:
                break
            else:
                continuar_agregando = input("¿Quieres agregar más columnas [S/N]?")
                if continuar_agregando.upper() == "S":
                    continue
                elif continuar_agregando.upper() == "N":
                    break

        query = self.cursor.execute("SELECT " + ", ".join(columnas_a_consultar) + " FROM " + ''.join(self.obtener_nombres_tablas()[self.tabla_seleccionada]) + ";")

        # Imprime los datos consultados en forma de tabla utilizando la biblioteca 'tabulate'
        tabla = tabulate(query.fetchall(), headers=columnas_a_consultar, tablefmt="fancy_grid" )
        print(tabla)
        
    def opcion_actualizar(self):
        pass
        # columna_actualizar : list = []
        # self.mostrar_tablas()
        # self.seleccionar_tabla()
        # self.mostrar_columnas()
        # while True:
        #     columna_elecionada = self.seleccionar_columna()
        #     if columna_elecionada == 0:
        #         print("Los ID no  se pueden modificar.")
        #     else:
        #         break
        # todas_columnas = self.cursor.execute(f"PRAGMA table_info({''.join(self.obtener_nombres_tablas()[self.tabla_seleccionada])});")
        
        # for columna in todas_columnas.fetchall():
        #         columna_actualizar.append(columna[1])
        # while True:
        #     modificacion = 
    def opcion_eliminar(self):
        self.mostrar_tablas()
        self.seleccionar_tabla()
        self.mostrar_columnas()
        selecionar_columna = self.seleccionar_columna()
        # TODO Hacer un bloque de codigo que traiga todas las columnas de la tabla.
        
        
        
        
        query = self.cursor.execute("DELETE FROM " +"".join(self.obtener_nombres_tablas()[self.tabla_seleccionada])+ " WHERE"+ +"="+ +";")# ? En cuanto puedas agrega los parametros faltantes entre los signos de mas

    def opciones(self):
        """Ofrece al usuario un menú de opciones para interactuar con la base de datos."""
        while True:
            try:
                eleccion = int(input("\n¿Qué deseas hacer hoy?\n1. Crear\n2. Leer\n3. Actualizar\n4. Eliminar\n5. Salir\nIngrese su elección: "))
            except ValueError:
                print("Debes elegir un número válido.")
                continue

            if eleccion == 1:
                self.opcion_crear_registro()
                decision_funcion = self.obtener_decision_seguir()
                if decision_funcion == 1:
                    print("Has elegido continuar.")
                    continue
                elif decision_funcion == 2:
                    print("Has salido del programa.")
                    break

            elif eleccion == 2:
                print("\nHas elegido Leer.".upper())
                self.opcion_leer()

                decision_funcion = self.obtener_decision_seguir()

                if decision_funcion == 1:
                    print("Has elegido continuar.")
                    continue
                elif decision_funcion == 2:
                    print("Has salido del programa.")
                    break

            elif eleccion == 3:
                print("\nHas elegido Actualizar.".upper())
                self.opcion_actualizar()

            elif eleccion == 4:
                print("\nHas elegido Eliminar.".upper())
                self.opcion_eliminar()
                
            elif eleccion == 5:
                print("Saliendo del programa.")
                self.cerrar_conexion()
                break
            else:
                print("Opción no válida. Por favor, elige una opción válida.")

if __name__ == "__main__":
    try:
        db_conex = CRUD('./db/cafe.db')
        db_conex.abrir_conexion()
        db_conex.opciones()
    except sqlite3.Error as e:
        print(f"Error al iniciar la aplicación: {e}")
