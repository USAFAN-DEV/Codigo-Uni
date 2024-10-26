#include "clientManager.h"
#include "filemanager.h"
#include "utils.h"

using namespace std;

FileManager::FileManager(){

    auto conn = initClient("127.0.0.1", 3001);
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

    auto conn = initClient("127.0.0.1", 3001);
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

    pack(buffer, (fileFuncs) listFilesF);
    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<fileFuncs>(buffer);

    if(ack != ackMSG){

        cout << "ERROR:" << __FILE__ << ":" << __LINE__ << endl;

    }

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