import Texto from '../../common/Texto.jsx';
import Imagen from '../../common/Imagen.jsx';
import ImagenLike from '../ImagenLike.jsx';
import SingleComic from './SingleComic.jsx';
import { getApiRequest } from '../../../api/apikey.js';
import { useState, useEffect, useRef } from 'react';

const RecentComics = () => {

    const queryResult = useRef([]); //Resultado de la query ejecutada al principio del programa
    const srcImagenClickada = useRef(''); //Src de la imagen del comicque tengo que mostrar en el popup (dialog) 
    const tituloImagenClickada = useRef(''); //Titulo del comic que tengo que mostrar en el popup (dialog)

    const [diccionarioComics, setDiccionarioComics] = useState({});  //Diccionario con [comic.title, comic.foto]
    const [descripcionComic, setDescripcionComic] = useState(''); //Estado con la descripcion del comic clickado
    const [diccionarioPersonajes, setDiccionarioPersonajes] = useState({}); //Diccionario con [personaje.nombre, personaje.foto]
    const [mostrarDialog, setMostrarDialog] = useState(false); //Estado para saber si hay que mostrar el dialog o no
    const [comicsFavoritos, setComicsFavoritos] = useState([]); //Array para guardar los comics favoritos
    
    //Cargamos los comics favoritos que haya almacenados en el localStorage
    useEffect(() => {

        let localStorageFavorites;
        const data = localStorage.getItem('comicsFavoritos');

        if(data){

            localStorageFavorites = JSON.parse(data); //Convertimos el string almacenado en un array

        }
        else{

            localStorageFavorites = [];

        }

        setComicsFavoritos(localStorageFavorites);
        
    }, []);

    //Obtenemos el diccionario [comic.titulo, comic.foto] de los comics recientes para mostrarlos
    useEffect(() => {

        getApiRequest('/v1/public/comics?orderBy=-modified&limit=10&dateDescriptor=thisMonth&')
        .then(result => result.data.results)
        .then(comics => {

            queryResult.current = comics;
            const nuevoDiccionarioComics = {};

            comics.forEach(comic => {

                if (comic.thumbnail.path && comic.title) {

                    if (comic.thumbnail.path !== "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available") {

                        nuevoDiccionarioComics[comic.title] = `${comic.thumbnail.path}/portrait_fantastic.${comic.thumbnail.extension}`;

                    }

                }

            });
            setDiccionarioComics(nuevoDiccionarioComics);

        });
    }, []);

    const handleFavoriteChange = (tituloComic) => {

        let updatedFavorites;

        if(comicsFavoritos.includes(tituloComic)){//Si el comic ya esta en favoritos, es que queremos eliminarlo

            updatedFavorites = comicsFavoritos.filter(comic => comic != tituloComic);

        }
        else{

            updatedFavorites = [...comicsFavoritos, tituloComic];

        }

        setComicsFavoritos(updatedFavorites);
        localStorage.setItem('comicsFavoritos', JSON.stringify(updatedFavorites));

    };

    const handleImageClick = (src) => {

        srcImagenClickada.current = src;
        let indexImagenClickada = -1;

        queryResult.current.forEach((comic, index) => {

            if (comic.thumbnail.path === src.slice(0, -23)) {

                indexImagenClickada = index;
                tituloImagenClickada.current = comic.title;

            }

        });

        if (indexImagenClickada !== -1) {

            setDescripcionComic(queryResult.current[indexImagenClickada].description);
            let newQuery = `${queryResult.current[indexImagenClickada].characters.collectionURI.slice(25)}?`;

            getApiRequest(newQuery).then(result => result.data.results).then(personajes => {

                const nuevoDiccionarioPersonajes = {};
                personajes.forEach(personaje => {

                    if (personaje.thumbnail.path && personaje.name) {

                        nuevoDiccionarioPersonajes[personaje.name] = `${personaje.thumbnail.path}/portrait_fantastic.${personaje.thumbnail.extension}`;

                    }

                });

                setDiccionarioPersonajes(nuevoDiccionarioPersonajes);

            });

        }

        setMostrarDialog(true);
    };

    const closeDialog = () => {

        setMostrarDialog(false);

    };

    const crearListaFavoritos = () => {

        
        if (comicsFavoritos.length === 0){

            return<p>No tienes cómics favoritos.</p>;

        } 
        else{

            return (

                <>

                    {comicsFavoritos.map((tituloComic) => (
                        
                        <div key={tituloComic} className="recent-comics-comic-container">

                            <Imagen onClick={handleImageClick} alt="fotoComic" src={diccionarioComics[tituloComic]} classNameContainer="recent-comics-comic-imagen-container"></Imagen>
                            <Texto contenido={tituloComic} classNameContainer="recent-comics-comic-titulo-container"></Texto>

                        </div>


                    ))}

                </>

            );
        }

    }

    return (
        <>
            <SingleComic mostrarDialog={mostrarDialog} imagenComic={srcImagenClickada.current} tituloComic={tituloImagenClickada.current}
                descripcionComic={descripcionComic}
                personajes={diccionarioPersonajes}
                cerrarDialog={closeDialog}
            ></SingleComic>

            <div id="recent-comics-titulo-container">

                <Texto contenido={"ULTIMAS NOVEDADES"} classNameContainer={"titulo-container"}></Texto>

            </div>

            <div id="recent-comics-data-container">

                {Object.entries(diccionarioComics).map(([tituloComic, fotoComic]) => (

                    <div key={tituloComic} className="recent-comics-comic-container">

                        <ImagenLike clave={fotoComic} classNameContainer="corazon-container" tituloComicCorrespondiente={tituloComic} onFavoriteChange={handleFavoriteChange}></ImagenLike>
                        <Imagen onClick={handleImageClick} alt="fotoComic" src={fotoComic} classNameContainer="recent-comics-comic-imagen-container"></Imagen>
                        <Texto contenido={tituloComic} classNameContainer="recent-comics-comic-titulo-container"></Texto>

                    </div>
                ))}

            </div>

            <Texto contenido={"COMICS FAVORITOS"} classNameContainer={"titulo-container"}></Texto>

            <div id="list-favorite-comics">

                
                {crearListaFavoritos()}

            </div>
        </>
    );
};

export default RecentComics;

