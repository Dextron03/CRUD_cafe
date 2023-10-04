import sqlite3
from conexion import Conexion
import conexion

class CRUD(Conexion):
    def __init__(self, name_db):
        super().__init__(name_db)

    def obtener_decision_seguir(self) -> int:
        """Este retorna un input el cual te permite seguir o salir del CRUD."""
        while True:
            while True:
                try:
                    seguir = int(input("\n¿Desea seguir con el proceso?:\nPara seguir, digite --> 1\nPara salir, digite --> 2\nIngrese su opción: "))
                    
                except ValueError:
                    seguir = print("\nLa respuesta debe ser un entero del 1 al 2, animal (ㆆ_ㆆ).")
                if isinstance(seguir, int):
                    break
                else:
                    continue
            if seguir == 1 or seguir == 2:
                break
            else:
                print("Respuesta invalida, intetalo.") 
                continue   
        return seguir
            

    def query_gr_tabla(self):
        """Busca las tablas que existen en la base de datos y retorna una lista con el nombre de las tablas."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        query = self.cursor.fetchall()
        return query
    
    def generar_tablas(self): #Agregar al codigo --> listo
        """Esta toma todas las tablas contenidas por la funcion query_gr_tabla y las imprime."""
        # Este bloque de codigo sirve para imprimir las tablas que hay en la base de datos.
        imprimir_query = self.query_gr_tabla()
        contador = 0
        for tablas in imprimir_query:
            contador = contador + 1
            print(f"{contador}.{''.join(tablas)}")

    def funtion_selec_table(self):
        """Esta contiene un input el cual permitira elegir la tabla con la que quieres trabajar."""
        while True:        
            try:
                selec_table : int = int(input(f"\n¿A que tabla desea insertarle datos? "))
                if isinstance(selec_table, int):
                    continue
                else:
                    break
            except ValueError:
                indices = [i for i in range(1,4,1)]
                self.generar_tablas()
                print(f"Porfavor Ingrese el numero/indice({indices} etc...).")
        return selec_table
    
    def opciones_crear(self):
        print("\nHas elegido Crear.")
        alm_query = self.query_gr_tabla()
        #Este bloque de codigo sirve para imprimir las tablas que hay en la base de datos.
        
        select_table = self.funtion_selec_table()
        
        #Crear/Insertar
        if select_table == 1:
            print("\nINSERTA LOS DATOS CORRESPONDIENTE:")
            nom_empleado : str = input("\tIngrese el nombre del empleado: ")
            ape_part_empleado : str = input(f"\tIngrese el apellido_paterno de {nom_empleado}: ")
            ape_mart_empleado : str = input(f"\tIngrese el apellido_materno de {nom_empleado}: ")
            edad_empleado : str = input(f"\tIngrese la edad del empleado: ")
            salario_empleado : int = int(input(f"\tIngrese el salario: "))
            self.cursor.execute(f"INSERT INTO "+"".join(alm_query[0])+f"(nombre_empleado, apellido_paterno, apellido_materno, edad, salario) VALUES('{nom_empleado}','{ape_part_empleado}','{ape_mart_empleado}','{edad_empleado}', '{salario_empleado}');")
            self.conn.commit()
            print(f"Registro insertado.".upper())
    
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
