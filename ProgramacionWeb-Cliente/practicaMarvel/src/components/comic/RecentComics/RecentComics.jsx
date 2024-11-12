import Texto from '../../common/Texto.jsx'
import Imagen from '../../common/Imagen.jsx'
import {getApiRequest} from '../../../api/apikey.js'
import { useState, useEffect } from 'react'

const queryRecentComics = "/v1/public/comics?orderBy=-modified&limit=16&dateDescriptor=thisMonth&";

const RecentComics = () => {

    const [diccionarioComics, setDiccionarioComics] = useState({});

    useEffect(() => {

        //TODO: HACER COMPROBACION SI NO EXISTE FOTO

        getApiRequest(queryRecentComics)
        .then(result =>{return result.data.results;})
        .then(comics => {

            //console.log(comics);

            const nuevoDiccionarioComics = {};

            comics.forEach(comic => {

                if(comic.thumbnail.path && comic.title){

                    console.log(comic.thumbnail.path);

                    if(comic.thumbnail.path != "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available"){

                        nuevoDiccionarioComics[comic.title] = `${comic.thumbnail.path}/portrait_fantastic.${comic.thumbnail.extension}`;

                    }

                }
                
            });
    
            setDiccionarioComics(nuevoDiccionarioComics);
            //console.log(nuevoDiccionarioComics);
    
        });

    }, []);

    return(

        <>

            <div id="recent-comics-titulo-container">

                <Texto contenido={"ULTIMAS NOVEDADES"} classNameContainer={"titulo-container"}></Texto>

            </div>

            <div id="recent-comics-data-container">

                {Object.entries(diccionarioComics).map(([tituloComic, fotoComic], index) => ( //Object.entries(diccionario) devuelve un array de pares [clave, valor]

                    <div key={tituloComic} className="recent-comics-comic-container">

                        <Imagen alt="fotoComic" src={fotoComic} classNameContainer="recent-comics-comic-imagen-container"></Imagen> 
                        <Texto contenido={tituloComic} classNameContainer="recent-comics-comic-titulo-container"></Texto>

                    </div>

                ))}

            </div>

        </>
        

    )

}

export default RecentComics;