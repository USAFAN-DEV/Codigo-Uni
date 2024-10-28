#include "conexionManager.h"
#include <cstdlib> 
#include <ctime>
using namespace std;

void conexionManager::atiendeConexion(int conexionId){

    brokerFuncs tipoMsg;
    std::vector<unsigned char> buffer;

    //recibimos el mensaje
    recvMSG(conexionId, buffer);

    //desempaquetamos el tipo de mensaje
    tipoMsg = unpack<brokerFuncs>(buffer);

    //si tipo mensaje:
    switch(tipoMsg){

        case serverConn:{
            
            string ipServer;

            cout << "Conexion con el server" << endl;

            //desempaquetar ip del server y almacenar
            ipServer.resize(unpack<int>(buffer));
            unpackv<char>(buffer, (char*)ipServer.data(), (int)ipServer.size());

            //almacenar ip
            conexions[conexions.size()] = ipServer;

            //mandamos el mensaje de ack al server
            buffer.clear();
            pack(buffer, (brokerFuncs)ackMSG2);

            break;
        }
        case clienteConn:{

            //tenemos que enviarle al cliente la ip del servidor

            cout << "Conexion con el cliente" << endl;

            //calculamos un numero random para decidir que servidor enviarle
            srand(static_cast<unsigned>(std::time(0)));
            int random_number = std::rand() % conexions.size();  // [0, numero de servidores almacenados)

            string ipServer = conexions[random_number];

            //empaquetamos el ack
            pack(buffer, (brokerFuncs)ackMSG2);

            //empaquetamos la ip del servidor
            pack(buffer, (int)ipServer.size());
            packv(buffer, (char*)ipServer.data(), (int)ipServer.size());

            break;
        }
        default:{

            std::cout << "ERROR: tipo de mensaje no valido\n";
            
            break;   
        }      

    }

    sendMSG(conexionId, buffer);

    closeConnection(conexionId);

}