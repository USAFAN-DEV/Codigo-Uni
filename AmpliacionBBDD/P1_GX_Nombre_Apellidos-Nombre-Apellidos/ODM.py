__author__ = 'Pablo Ramos Criado'
__students__ = 'Nicolas_Graullera'


from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from typing import Generator, Any, Self
from geojson import Point
import pymongo
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor
import yaml
import json
from datetime import datetime


def getLocationPoint(address: str) -> Point:
    """ 
    Obtiene las coordenadas de una dirección en formato geojson.Point
    Utilizar la API de geopy para obtener las coordenadas de la direccion
    Cuidado, la API es publica tiene limite de peticiones, utilizar sleeps.

    Parameters
    ----------
        address : str
            direccion completa de la que obtener las coordenadas
    Returns
    -------
        geojson.Point
            coordenadas del punto de la direccion
    """
    location = None

    while location is None:

        try:
            #Se puede utilizar un nombre aleatorio para user_agent
            location = Nominatim(user_agent="Gravyy", timeout = 10).geocode(address)

            if location:

                return Point((location.longitude, location.latitude))
            else:
                print(f"ERROR. No se encontraron las cordenadas de {address}")
                return None
        
        except GeocoderTimedOut as e:
            #Volvemos a intentarlo
            print(e)
            continue

    

class Model:
    """ 
    Clase de modelo abstracta
    Crear tantas clases que hereden de esta clase como  
    colecciones/modelos se deseen tener en la base de datos.

    Attributes
    ----------
        required_vars : set[str]
            conjunto de variables requeridas por el modelo
        admissible_vars : set[str]
            conjunto de variables admitidas por el modelo
        db : pymongo.collection.Collection
            conexion a la coleccion de la base de datos
    
    Methods
    -------
        __setattr__(name: str, value: str | dict) -> None
            Sobreescribe el metodo de asignacion de valores a las
            variables del objeto con el fin de controlar las variables
            que se asignan al modelo y cuando son modificadas.
        save()  -> None
            Guarda el modelo en la base de datos
        delete() -> None
            Elimina el modelo de la base de datos
        find(filter: dict[str, str | dict]) -> ModelCursor
            Realiza una consulta de lectura en la BBDD.
            Devuelve un cursor de modelos ModelCursor
        aggregate(pipeline: list[dict]) -> pymongo.command_cursor.CommandCursor
            Devuelve el resultado de una consulta aggregate.
        find_by_id(id: str) -> dict | None
            Busca un documento por su id utilizando la cache y lo devuelve.
            Si no se encuentra el documento, devuelve None.
        init_class(db_collection: pymongo.collection.Collection, required_vars: set[str], admissible_vars: set[str]) -> None
            Inicializa las variables de clase en la inicializacion del sistema.

    """
    required_vars: set[str]
    admissible_vars: set[str]
    db: Collection

    def __init__(self, **kwargs: dict[str, str | dict]):
        """
        Inicializa el modelo con los valores proporcionados en kwargs
        Comprueba que los valores proporcionados en kwargs son admitidos
        por el modelo y que las variables requeridas son proporcionadas.

        Parameters
        ----------
            kwargs : dict[str, str | dict]
                diccionario con los valores de las variables del modelo
        """

        #Comprobamos que los atributos introducidos son validos
        
        for var in self.required_vars: #Comprobamos si las variables obligatorias han sido introducidas
            
            if var not in kwargs:

                raise ValueError (f"ERROR. La variable '{var}' es una variable obligatoria. Intente crear el objeto de nuevo.")
            
        for var in kwargs: #Comprobamos si las variables introducidas corresponden con las variables del modelo

            if not self.validate_vars(var):
                
                raise ValueError (f"ERROR. La variable '{var}' no corresponde con este modelo. Intente crear el objeto de nuevo.")
            
        self.__dict__.update(kwargs)  #Actualiza los valores de los atributos de la clase con los valores guardados en kwargs

    def validate_vars(self, var_name:str) -> bool:
        """
        Funcion para comprobar que una variable pertenece a las variables permitidas para un modelo

        Parameters
        ----------
            var_name:str
                nombre de la variable
        """

        if var_name not in self.admissible_vars and var_name not in self.required_vars:

            return False

        return True

    def __setattr__(self, name: str, value: str | dict) -> None:
        """ Sobreescribe el metodo de asignacion de valores a las 
        variables del objeto con el fin de controlar las variables
        que se asignan al modelo y cuando son modificadas.
        """
   
        #Comprobamos que la variable que se quiere añadir o actualizar se permite en el modelo
        if not self.validate_vars(name):

            raise ValueError (f"ERROR. Estas intentando asignar un valor al atributo {name} que no existe en este modelo")

        # Asigna el valor value a la variable name
        self.__dict__[name] = value
        
    def save(self) -> None:
        """
        Guarda el modelo en la base de datos
        Si el modelo no existe en la base de datos, se crea un nuevo
        documento con los valores del modelo. En caso contrario, se
        actualiza el documento existente con los nuevos valores del
        modelo.
        """

        #TODO

        #Comprobamos que la conexion a la db existe
        if self.db is None:
            raise ValueError("ERROR: No hay conexión a la base de datos.")

        data = {}

        for var in self.admissible_vars.union(self.required_vars):

            if var in self.__dict__:

                data[var] = self.__dict__[var]

        if "_id" in self.__dict__:

            result = self.db.update_one({"_id": self.__dict__["_id"]}, {"$set": data})

        else:

            result = self.db.insert_one(data)
            self.__dict__["_id"] = result.inserted_id

    def delete(self) -> None:
        """
        Elimina el modelo de la base de datos
        """
        
        #Comprobamos que la conexion a la db existe
        if self.db is None:
            raise ValueError("ERROR: No hay conexión a la base de datos.")
        
        self.db.drop()
    
    @classmethod
    def find(cls, filter: dict[str, str | dict]) -> Any:
        """ 
        Utiliza el metodo find de pymongo para realizar una consulta
        de lectura en la BBDD.
        find debe devolver un cursor de modelos ModelCursor

        Parameters
        ----------
            filter : dict[str, str | dict]
                diccionario con el criterio de busqueda de la consulta
        Returns
        -------
            ModelCursor
                cursor de modelos
        """ 

        cursor = cls.db.find(filter)
        return ModelCursor(cls, cursor)
    
    @classmethod
    def aggregate(cls, pipeline: list[dict]) -> CommandCursor:
        """ 
        Devuelve el resultado de una consulta aggregate. 
        No hay nada que hacer en esta funcion.
        Se utilizara para las consultas solicitadas
        en el segundo proyecto de la practica.

        Parameters
        ----------
            pipeline : list[dict]
                lista de etapas de la consulta aggregate 
        Returns
        -------
            pymongo.command_cursor.CommandCursor
                cursor de pymongo con el resultado de la consulta
        """ 
        return cls.db.aggregate(pipeline)
    
    @classmethod
    def find_by_id(cls, id: str) -> Self | None:
        """ 
        NO IMPLEMENTAR HASTA EL TERCER PROYECTO
        Busca un documento por su id utilizando la cache y lo devuelve.
        Si no se encuentra el documento, devuelve None.

        Parameters
        ----------
            id : str
                id del documento a buscar
        Returns
        -------
            Self | None
                Modelo del documento encontrado o None si no se encuentra
        """ 
        #TODO
        pass

    @classmethod
    def init_class(cls, db_collection: pymongo.collection.Collection, required_vars: set[str], admissible_vars: set[str]) -> None:
        """ 
        Inicializa las variables de clase en la inicializacion del sistema.
        En principio nada que hacer aqui salvo que se quieran realizar
        alguna otra inicialización/comprobaciones o cambios adicionales.

        Parameters
        ----------
            db_collection : pymongo.collection.Collection
                Conexion a la collecion de la base de datos.
            required_vars : set[str]
                Set de variables requeridas por el modelo
            admissible_vars : set[str] 
                Set de variables admitidas por el modelo
        """
        cls.db = db_collection
        cls.required_vars = required_vars
        cls.admissible_vars = admissible_vars
        

class ModelCursor:
    """ 
    Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.

    Attributes
    ----------
        model_class : Model
            Clase para crear los modelos de los documentos que se iteran.
        cursor : pymongo.cursor.Cursor
            Cursor de pymongo a iterar

    Methods
    -------
        __iter__() -> Generator
            Devuelve un iterador que recorre los elementos del cursor
            y devuelve los documentos en forma de objetos modelo.
    """

    def __init__(self, model_class: Model, cursor: pymongo.cursor.Cursor):
        """
        Inicializa el cursor con la clase de modelo y el cursor de pymongo

        Parameters
        ----------
            model_class : Model
                Clase para crear los modelos de los documentos que se iteran.
            cursor: pymongo.cursor.Cursor
                Cursor de pymongo a iterar
        """
        self.model = model_class
        self.cursor = cursor
    
    def __iter__(self) -> Generator:
        """
        Devuelve un iterador que recorre los elementos del cursor
        y devuelve los documentos en forma de objetos modelo.
        Utilizar yield para generar el iterador
        Utilizar la funcion next para obtener el siguiente documento del cursor
        Utilizar alive para comprobar si existen mas documentos.
        """
        while self.cursor.alive:

            doc = next(self.cursor)
            yield self.model(**doc)
            
        #Al usar **doc, el diccionario se desempaqueta en pares de clave-valor que coinciden con los argumentos que espera el constructor del modelo. 
 



def initApp(definitions_path: str = "./models.yml", mongodb_uri="mongodb://localhost:27017/", db_name="abd") -> None:
    """ 
    Declara las clases que heredan de Model para cada uno de los 
    modelos de las colecciones definidas en definitions_path.
    Inicializa las clases de los modelos proporcionando las variables 
    admitidas y requeridas para cada una de ellas y la conexión a la
    collecion de la base de datos.
    
    Parameters
    ----------
        definitions_path : str
            ruta al fichero de definiciones de modelos
        mongodb_uri : str
            uri de conexion a la base de datos
        db_name : str
            nombre de la base de datos
    """

    # Inicializar base de datos
    try:

        client = pymongo.MongoClient(mongodb_uri)

    except Exception:

        print("ERROR. " + Exception)

    database = client[db_name] #Todavia no se crea la base de datos. Solo accede a ella. Se crea cuando se realize una operacion en ella
                               #Si la base de datos ya ha sido creada, mongo la devuelve, y no crea otra nueva.

    # Declarar tantas clases modelo colecciones existan en la base de datos
    # Leer el fichero de definiciones de modelos para obtener las colecciones
    # y las variables admitidas y requeridas para cada una de ellas.
    # Ejemplo de declaracion de modelo para colecion llamada MiModelo

    with open("./models.yml", "r") as file:

        config = yaml.safe_load(file)

    model_names = list(config["Model"].keys())

    for model_name in model_names:

        globals()[model_name] = type(model_name, (Model,), {})
        globals()[model_name].init_class(database[model_name], set(config["Model"][model_name]["required_vars"]), set(config["Model"][model_name]["admissible_vars"]))
        
    # Ignorar el warning de Pylance sobre MiModelo, es incapaz de detectar
    # que se ha declarado la clase en la linea anterior ya que se hace
    # en tiempo de ejecucion.

    return globals()
 



# TODO 
# PROYECTO 2
# Almacenar los pipelines de las consultas en Q1, Q2, etc. 
# EJEMPLO
# Q0: Listado de todas las personas con nombre determinado
nombre = "Quijote"
Q0 = [{'$match': {'nombre': nombre}}]

# Q1: 
Q2 = []

# Q2: 
Q2 = []

# Q3:
Q3 = []

# Q4: etc.


if __name__ == '__main__':

    #delete
    
    # Inicializar base de datos y modelos con initApp
    initApp()

    # Creamos los modelos
    addresses = ["1600 Amphitheatre Parkway, Mountain View, CA, USA", "1 Infinite Loop, Cupertino, CA, USA", "350 Fifth Avenue, New York, NY, USA", "5th Avenue, New York, NY, USA",
    "350 10th Ave, New York, NY, USA", "101 N. Wacker Dr, Chicago, IL, USA", "6000 S Las Vegas Blvd, Las Vegas, NV, USA", "30 Rockefeller Plaza, New York, NY, USA",
    "12 S 12th St, Philadelphia, PA, USA", "1 Disneyland Dr, Anaheim, CA, USA"]
    nombres = ["Nicolas", "Alice", "Bob", "Sofia", "Liam", "Emma", "Oliver", "Mia", "Ethan", "Ava"]
    numeros = [12345678, 87654321, 23456789, 98765432, 34567890, 45678901, 56789012, 67890123, 78901234, 89012345]
    nombre_productos = ["Laptop", "Smartphone", "Auriculares Bluetooth", "Televisor 4K", "Reloj inteligente", "Cámara DSLR", "Tablet", "Altavoz inteligente", "Monitor LED", "Impresora multifuncional"]
    precios = [199.99, 899.99, 129.49, 499.99, 249.00, 349.99, 199.99, 79.99, 599.99, 49.99]
    nombre_proveedores = ["Modas paqui","Tech Solutions", "Innovative Electronics", "Gadgets R Us", "Smart Home Supplies", "Digital World", "ElectroMart", "Future Gadgets", "Premium Devices", "Global Tech Supply", "NextGen Innovations"]

    clientes = []
    productos = []
    compras = []
    proveedores = []

    for i in range(10):
        clientes.append(Cliente(nombre = nombres[i], direccion_de_facturacion = getLocationPoint(addresses[i]), direccion_de_envio = getLocationPoint(addresses[i]), tarjeta_de_pago = numeros[i]))
        productos.append(Producto(nombre = nombre_productos[i], codigo_del_producto = numeros[i], precio_con_iva = precios[i]))
        compras.append(Compra(cliente = nombres[i], precio_compra = precios[i], direccion_envio = getLocationPoint(addresses[i])))
        proveedores.append(Proveedor(nombre = nombre_proveedores[i], direccion_almacenes = getLocationPoint(addresses[i])))

    for i in range(10):
        clientes[i].save()
        productos[i].save()
        compras[i].save()
        proveedores[i].save()

    #mongoexport --uri "mongodb://localhost:27017/mi_base_de_datos" --collection usuarios --out usuarios.json
    #mongoimport --db myDatabase --collection myCollection --file data.json --jsonArray



    # PROYECTO 2
    # Ejecutar consultas Q1, Q2, etc. y mostrarlo
    #TODO
    #Ejemplo
    #Q1_r = MiModelo.aggregate(Q1)





