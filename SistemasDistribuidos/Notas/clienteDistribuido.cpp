using namespace std;


FileManager::FileManager(){

    auto conn = initClient("127.0.0.1", 3001);
    vector<unsigned char> buffer;

    pack(buffer, (serverFuncs)FileManagerConstructor);
    sendMSG(conn.serverId, buffer);
    buffer.clear();
    recvMSG(conn.serverId, buffer);

    auto ack = unpack<serverFuncs>(buffer);

    if(ack != ackMSG){
        
        print(error)

    }
    else{

        clientManager::connectionsIds[this] == conn;

        //si fuese una funcion de getAlgo

    }

}