import sqlite3
from conexion import Conexion
import conexion

class CRUD(Conexion):
    def __init__(self, name_db):
        super().__init__(name_db)

    def obtener_decision_seguir(self):
        while True:
            try:
                seguir = int(input("¿Desea seguir con el proceso?:\nPara seguir, digite --> 1\nPara salir, digite --> 2\nIngrese su opción: "))
            
            except ValueError:
                print("\nLa respuesta debe ser un entero del 1 al 2, animal (ㆆ_ㆆ).")
            if isinstance(seguir, int):
                break
        return seguir

    def query_gr_tabla(self):
        """Busca las tablas que existen en la base de datos y retorna una lista con el nombre de las tablas."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        query = self.cursor.fetchall()
        return query
    
    # def generar_tablas(self): Agregar al codigo
    #     # Este bloque de codigo sirve para imprimir las tablas que hay en la base de datos.
    #     contador = 0
    #     for tablas in self.query:
    #         contador = contador + 1
    #         print(f"{contador}.{''.join(tablas)}")

    def opciones_crear(self):
        print("\nHas elegido Crear.")
        alm_query = self.query_gr_tabla()
        #Este bloque de codigo sirve para imprimir las tablas que hay en la base de datos.
        contador = 0
        for tablas in alm_query:
            contador = contador + 1
            print(f"{contador}.{''.join(tablas)}") 
            
        selec_table : str = int(input(f"¿A que tabla desea insertarle datos? "))
        
        #Crear/Insertar
        if selec_table == 1:
            nom_empleado : str = input("Ingrese el nombre del empleado: ")
            ape_part_empleado : str = input(f"Ingrese el apellido_paterno de {nom_empleado}: ")
            ape_mart_empleado : str = input(f"Ingrese el apellido_materno de {nom_empleado}: ")
            edad_empleado : str = input(f"Ingrese la edad del empleado: ")
            salario_empleado : int = int(input(f"Ingrese el salario: "))
            self.cursor.execute(f"INSERT INTO "+"".join(alm_query[0])+f"(nombre_empleado, apellido_paterno, apellido_materno, edad, salario) VALUES('{nom_empleado}','{ape_part_empleado}','{ape_mart_empleado}','{edad_empleado}', '{salario_empleado}');")
            self.conn.commit()
    
    def opciones(self):
        while True:    
            try:#Este bloque de codigo permite que el usuario ingrese una opción numérica, y si el usuario ingresa algo que no se puede convertir en un entero, se muestra un mensaje de error y se le da la oportunidad de ingresar una entrada válida.
                opcion = int(input("\n¿Qué quieres hacer hoy?\n1. Crear\n2. Leer\n3. Actualizar\n4. Eliminar\n5. Salir\n6. Buscar\nDijite su opcion: "))
            except ValueError:
                    print("Debes elegir un número válido.")
                    continue
             
            if  opcion== 1:
                self.opciones_crear()
                decision_funcion = self.obtener_decision_seguir()
                
                if decision_funcion == 1:
                   print("Haz elegido seguir.")
                   continue
                elif decision_funcion == 2:
                   print("Haz salido del programa.")
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
