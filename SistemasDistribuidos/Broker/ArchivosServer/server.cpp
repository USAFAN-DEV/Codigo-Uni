#include "utils.h"
#include <iostream>
#include <string>
#include <thread>
#include <list>
#include "clientManager.h"
#include "conexionManager.h"
using namespace std;

int main(int argc, char** argv){

    //init server
    int serverSocketID = initServer(3001);
    cout << "initServer" << endl;

    if(argc == 2){

        //init conexion con el broker
        auto conn = initClient("98.82.195.21", 3001);

        //obtener la ip, empaquetarla y mandarsela al broker
        vector<unsigned char> buffer;
        string ip_server = argv[1];

        //empaquetamos lo que queremos hacer
        pack(buffer, (brokerFuncs)serverConn);

        //empaquetamos la ip del server
        pack(buffer, (int)ip_server.size());
        packv(buffer, (char*)ip_server.data(), (int)ip_server.size());

        //mandamos el mensaje al broker
        sendMSG(conn.serverId, buffer);
        buffer.clear();

        //comprobamos que el mensaje ha llegado
        recvMSG(conn.serverId, buffer);

        auto ack = unpack<brokerFuncs>(buffer);
        if(ack != ackMSG2){

            cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

        }
        else{

            cout << "Conexion establecida con el broker, ip enviada correctamente" << endl;
            closeConnection(conn.serverId); //Revisar que no pete el programa

        }

        while(1){

            while(!checkClient()) usleep(100);

            cout << "Cliente conectado" << endl;

            int clientId = getLastClientID();

            thread *th = new thread(clientManager::atiendeCliente, clientId);

        }

        close(serverSocketID);
        return 0;
    }

}
