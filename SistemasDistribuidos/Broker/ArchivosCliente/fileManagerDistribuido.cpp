#include "clientManager.h"
#include "filemanager.h"
#include "conexionManager.h"
#include "utils.h"

using namespace std;

string FileManager::obtenerIpServer(string ipBroker){

    string ipServer;

    auto conn = initClient(ipBroker, 3001);
    vector <unsigned char> buffer;

    //empaquetamos y enviamos el mensaje para solicitar una ip
    pack(buffer, (brokerFuncs)clienteConn);
    sendMSG(conn.serverId, buffer);

    buffer.clear();
    recvMSG(conn.serverId, buffer);

    //cerramos la conexion con el broker, ya hemos obtenido lo que queriamos. Revisar que no pete el programa
    closeConnection(conn.serverId);

    //comprobamos que la peticion ha sido atendida
    auto ack = unpack<brokerFuncs>(buffer);

    if(ack != ackMSG2){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;
        return "ERROR";

    }
    else{

        //desempaquetamos la ip del servidor
        ipServer.resize(unpack<int>(buffer));
        unpackv(buffer, (char*)ipServer.data(), (int)ipServer.size());
        return ipServer;

    }

}

FileManager::FileManager(){

    //obtenemos la ip del servidor
    string ipServer = obtenerIpServer("98.82.195.21");

    auto conn = initClient(ipServer, 3001);
    vector <unsigned char> buffer;

    pack(buffer, (fileFuncs)FileManagerF);
    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }
    else{

        clientManager::connectionIds[this] = conn;

    }

}

FileManager::FileManager(string path){

    //obtenemos la ip del servidor
    string ipServer = obtenerIpServer("98.82.195.21");

    auto conn = initClient(ipServer, 3001);
    vector <unsigned char> buffer;

    //empaquetamos ack
    pack(buffer, (fileFuncs) FileManagerParamsF);

    //empaquetamos el path
    pack(buffer, (int)path.size());
    packv(buffer, (char*)path.data(), (int)path.size());

    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }
    else{

        clientManager::connectionIds[this] = conn;

    }
    
}

FileManager::~FileManager(){

    auto conn = clientManager::connectionIds[this];
    vector<unsigned char> buffer;

    pack(buffer, (fileFuncs)FileManagerDF);

    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }

    closeConnection(conn.serverId);

}

vector<string> FileManager::listFiles(){

    auto conn = clientManager::connectionIds[this];
    vector<unsigned char> buffer;
    vector<string> files;

    pack(buffer, (fileFuncs) listFilesF);
    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }
    else{

        files.resize(unpack<int>(buffer));

        for(int i = 0; i < files.size(); i++){

            files[i].resize(unpack<int>(buffer));
            unpackv<char>(buffer, (char*)files[i].data(), (int)files[i].size());

        }

    }

    return files;

}

void FileManager::readFile(string fileName, vector<unsigned char> &data){

    auto conn = clientManager::connectionIds[this];
    vector<unsigned char> buffer;

    pack(buffer, (fileFuncs)readFilesF);
    pack(buffer, (int)fileName.size());
    packv(buffer, (char*)fileName.data(), (int)fileName.size());

    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }
    else{

        data.resize(unpack<int>(buffer));
        unpackv<char>(buffer, (char*)data.data(), (int)data.size());

    }

}

void FileManager::writeFile(string fileName, vector<unsigned char> &data){

    auto conn = clientManager::connectionIds[this];
    vector<unsigned char> buffer;

    pack(buffer, (fileFuncs)writeFilesF);

    pack(buffer, (int)fileName.size());
    packv(buffer, (char*)fileName.data(), (int)fileName.size());

    pack(buffer, (int)data.size());
    packv(buffer, (char*)data.data(), (int)data.size());

    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }

}