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
		
			static inline map<int, FileManager> clients;
			static inline map<FileManager*,connection_t > connectionIds;
			
			
			
			static inline bool salir=false;			
			static void atiendeCliente(int clientId);
};