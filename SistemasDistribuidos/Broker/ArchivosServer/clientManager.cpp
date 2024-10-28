#include "clientManager.h"
#include "filemanager.h"

using namespace std;

void clientManager::atiendeCliente(int clientId){

    fileFuncs tipoMsg;
    std::vector<unsigned char> buffer;

    do{

        //recibimos el mensaje
        recvMSG(clientId, buffer);

        //desempaquetamos el tipo de mensaje
        tipoMsg = unpack<fileFuncs>(buffer);

        //si tipo mensaje:
        switch(tipoMsg){

            case FileManagerF:{
                
                //Creamos la persona
                FileManager f;

                //Almacenamos la nueva persona
                clients[clientId] = f;
                buffer.clear();
                pack(buffer, ackMSG); //ackMSG: para comprobar que te han llegado bien los datos, el cliente recibe el buffer con el ackMSG para comprobar que te ha llegado bien la informacion

                break;
            }

            case FileManagerParamsF:{

                string path;

                //unpackv para arrays y strings
                path.resize(unpack<int>(buffer)); //resize = realloc
                unpackv<char>(buffer, (char*)path.data(), path.size()); //buffer, nombre donde se guarda, tamaño.
                //(char*)nombre.data(): Esto obtiene un puntero a la memoria subyacente de la cadena nombre. Al hacer un cast a char*, se permite que unpackv escriba directamente en la memoria de la cadena.   

                //creamos la persona
                FileManager f(path);

                //almacenamos la nueva persona
                clients[clientId] = f;
                buffer.clear();
                pack(buffer, ackMSG);

                break;
            }

            case FileManagerDF:{

                clients.erase(clientId);
                buffer.clear();
                pack(buffer, ackMSG);

                break;
            }

            case listFilesF:{

                std::vector<string> files;
                files = clients[clientId].listFiles();

                //empaquetamos el ack
                pack(buffer, (fileFuncs)ackMSG);

                //empaquetamos el tamanio del array
                pack(buffer, (int)files.size());

                //recorremos cada string del array
                for(int i = 0; i < files.size(); i++){

                    //empaquetamos el tamanio del string
                    pack(buffer, (int)files[i].size());

                    //empaquetamos el string
                    packv(buffer, (char*)files[i].data(), (int)files[i].size());

                }

                break;
            }

            case writeFilesF:{

                string fileName;
                std::vector <unsigned char> data;

                //resize al string
                fileName.resize(unpack<int>(buffer));
                //desempaquetamos el string 
                unpackv<char>(buffer, (char*)fileName.data(), (int)fileName.size());

                data.resize(unpack<int>(buffer));
                unpackv<char>(buffer, (char*)data.data(), (int)data.size());

                clients[clientId].writeFile(fileName, data);

                buffer.clear();
                pack(buffer, (fileFuncs)ackMSG);

                break;
            }
            
            case readFilesF:{

                string fileName;
                std::vector<unsigned char> data;

                fileName.resize(unpack<int>(buffer));
                unpackv<char>(buffer, (char*)fileName.data(), (int)fileName.size());

                clients[clientId].readFile(fileName, data);

                buffer.clear();
                pack(buffer, fileFuncs(ackMSG));
                
                pack(buffer, (int)data.size());
                packv(buffer, (char*)data.data(), (int)data.size());

                break;
            }

            default:{

                std::cout << "ERROR: tipo de mensaje no valido\n";
                
                break;   
            }      

        }

        sendMSG(clientId, buffer);

    }while(tipoMsg != FileManagerDF);
    closeConnection(clientId);

}