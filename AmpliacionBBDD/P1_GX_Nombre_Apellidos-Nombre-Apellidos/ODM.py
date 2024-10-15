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


def get_geojson_point(latitud: int, longitud: int):
    """
    Obtiene un GeoJSON de tipo punto con la latitud y longitud almacenados

    Parameters
    ----------
        latitud: int
        longitud: int
    Returns
    -------
        json formatted string
            Contiene la informacion del punto (longitud y latitud)
    """

    geojson_point = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitud, latitud]
        },
        "properties":{}
    }

    return json.dumps(geojson_point, indent=2)

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

                return get_geojson_point(location.latitude, location.longitude)
            else:
                print(f"ERROR. No se encontro la direccion {address}")
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

            raise ValueError ("ERROR. Estas intentando asignar un valor a un atributo que no existe en este modelo")

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

        #Comprobamos que la conexion a la db existe
        if self.db is None:
            raise ValueError("ERROR: No hay conexión a la base de datos.")

        # Convertir el objeto a un diccionario para guardar
        #data = {var: self.__dict__[var] for var in self.admissible_vars.union(self.required_vars) if var in self.__dict__}

        data = {}

        for var in self.admissible_vars.union(self.required_vars):

            if var in self.__dict__:

                data[var] = self.__dict__[var]
        
        # Insertar el documento
        result = self.db.insert_one(data)
        #print(f"Documento insertado con ID: {result.inserted_id}")

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
            if doc:

                yield self.model(**doc)

            else:

                break


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

    if db_name not in client.list_database_names():

        raise ValueError(f"ERROR: La base de datos '{db_name}' no existe.")

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
    
    # Inicializar base de datos y modelos con initApp
    initApp()

    """
    Ejemplo
    m = Model(nombre="Pablo", apellido="Ramos", edad=18)
    m.save()
    m.nombre="Pedro"
    print(m.nombre)
    """

    # Hacer pruebas para comprobar que funciona correctamente el modelo

    # Crear modelo
    cliente = Cliente(nombre = "Nicolas", direccion_de_facturacion = "175 5th Avenue NYC", direccion_de_facturacion_GeoJson = getLocationPoint("175 5th Avenue NYC"), direccion_de_envio = "11111 Euclid Ave", direccion_de_envio_GeoJson = getLocationPoint("11111 Euclid Ave"), tarjeta_de_pago = 12345678) # type: ignore
    # Asignar nuevo valor a variable admitida del objeto 
    setattr(cliente, "fecha_de_alta", datetime(2024, 10, 14, 16, 14, 0, 0))

    # Asignar nuevo valor a variable no admitida del objeto 
    try:
        setattr(cliente, "fecha_inventada", datetime(2024, 10, 14, 16, 14, 0, 0))
    except ValueError as e:
        print(e)

    # Guardar
    cliente.save()

    # Asignar nuevo valor a variable admitida del objeto
    setattr(cliente, "fecha_de_ultimo_acceso", datetime(2024, 10, 12, 10, 0, 0, 0))

    # Guardar
    cliente.save()

    # Buscar nuevo documento con find
    doc_cursor = cliente.find({}).__iter__()

    # Obtener primer documento
    for doc in doc_cursor:
        print(doc)
        
    # Modificar valor de variable admitida
    fecha_de_ultimo_acceso = datetime.now()

    # Guardar
    cliente.save()

    # PROYECTO 2
    # Ejecutar consultas Q1, Q2, etc. y mostrarlo
    #TODO
    #Ejemplo
    #Q1_r = MiModelo.aggregate(Q1)





