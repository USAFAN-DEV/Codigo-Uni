#pragma once
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <experimental/filesystem> 
#include <fstream> 
#include <iostream> 
#include <iterator>

using namespace std;
using namespace std::experimental::filesystem; 

class FileManager
{
	private:
		string dirPath;
		bool ready=false;
	public:
		/**
		* @brief FileManager::FileManager Constructor sin parámetros de la clase FileManager (vacío). 
		*
		*/
	
		FileManager();
		/**
		* @brief FileManager::FileManager Destructor sin parámetros de la clase FileManager (vacío). 
		*
		*/
		~FileManager();
		/**
		* @brief FileManager::FileManager Constructor de la clase FileManager. Recibe por parámetros el directorio
		* que usará esta clase para indexar, almacenar y leer ficheros. Se aconseja usar una ruta completa al directorio,
		* desde la raiz del sistema de ficheros.
		*
		* @param path Ruta al directorio que se desea usar
		*/
		FileManager(string path);
		/**
		 * @brief FileManager::obtenerIpServer es una funcion para obtener la ip de un servidor al que conectarse. 
		 * 
		 * @param ipBroker direccion IP del broker al que se conecta el cliente para obtener la IP de un servidor
		 * 
		 * @return La direccion IP del servidor
		 */
		string obtenerIpServer(string ipBroker);
		/**
		 * @brief FileManager::listFiles Sirve para acceder a la lista de ficheros almacenados en la ruta
		 * que se usó en el contructor de la clase. Únicamente lista ficheros, los directorios son ignorados
		 * @return Una copia de la lista de ficheros
		 */
		vector<string> listFiles();
		/**
		 * @brief FileManager::readFile Dado el nombre de un fichero almacenado en el directorio que se usó en el contructor,
		 * se inicializará la variable "data" con el contenido del fichero
		 *
		 * @param fileName Nombre del fichero a leer
		 * @param data Datos del fichero
		 */
		void readFile(string fileName, vector<unsigned char> &data);
		/**
		 * @brief FileManager::readFile Dado un nuevo nombre de un fichero que se quiere almacenar en el directorio que se usó en el contructor,
		 * se escribirá el contenido del array de datos almacenado en "data". Sobreescribirá el fichero que hubiera en el directorio si tiene el mismo nombre.
		 *
		 * @param fileName Nombre del fichero a escribir
		 * @param data Datos del fichero.
		 */
		void writeFile(string fileName, vector<unsigned char> &data);
};
