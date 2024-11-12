using namespace std;

void clientManager::atiendeCliente(int clientId){

    serverFuncs tipoMensaje;
    vector<unsigned char> buffer;

    //recibir mensaje
    recvMSG(clientId, buffer);

    //desempaquetar mensaje
    tipoMensaje = unpack<serverFuncs>(buffer);

    //se puede implementar un do while si queremos que el cliente permanezca conectado al servidor o no si solo necesita hacer una unica peticion

    switch(tipoMensaje){


        case tipoMensaje1:{


            break;
        }
        case tipoMensaje2:{


            break;
        }
        default:{

            print("Error");

            break;
        }

    }

    //mandamos mensaje
    sendMSG(clientId, buffer);

    //cerramos conexion con el cliente
    closeConnection(clientId);

}

//EJEMPLO LIBRERIA

#pragma once
#include "utils.h"
#include "filemanager.h"
using namespace std;
typedef enum{

	FileManagerF,//constructor defecto
	FileManagerParamsF,//constructor parametros
	FileManagerDF,//destructor
	listFilesF,
	writeFilesF,
	readFilesF,
	
	ackMSG
}fileFuncs;

class clientManager{

		public:
		
			static inline map<int, FileManager> clients; //ALMACENAMOS LOS CLIENTES CON SUS DATOS
			static inline map<FileManager*,connection_t > connectionIds; //ALMACENAMOS LAS CONEXIONES
			
			static inline bool salir=false;			
			static void atiendeCliente(int clientId);
};