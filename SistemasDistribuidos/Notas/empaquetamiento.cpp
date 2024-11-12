//EMPAQUETAR STRINGS / vector <unsigned char>

string nombre;
vector<unsigned char> buffer;

pack(buffer, (int)nombre.size());
packv(buffer, (char*)nombre.data(), (int)nombre.size());

//EMPAQUETAR ARRAY

vector<string> nombres;
vector<unsigned char> buffer;

//empaquetamos el tamanio del array
pack(buffer, (int)nombres.size());

//por cada string, empaquetamos su tamanio y su contenido
for(int i = 0; i < nombres.size(); i++){

    pack(buffer, (int)nombres[i].size());
    packv(buffer, (char*)nombres[i].data(), (int) nombres[i].data());

}

//EMPAQUETAR OTRA COSA
vector<unsigned char> buffer;

pack(buffer, (int)edad);

//DESEMPAQUETAR STRINGS
vector<unsigned char> buffer;
string nombre;

nombre.resize(unpack<int>(buffer));
unpackv<char>(buffer, (char*)nombre.data(), (int)nombre.size());

//DESEMPAQUETAR ARRAY
vector<unsigned char> buffer;
vector<string> nombres;

nombres.resize(unpack<int>(buffer));

for(int i = 0; i < nombres.size(); i++){

    nombres[i].resize(unpack<int>(buffer));
    unpackv<char>(buffer, (char*)nombres[i].data(), (int)nombres[i].size());

}

