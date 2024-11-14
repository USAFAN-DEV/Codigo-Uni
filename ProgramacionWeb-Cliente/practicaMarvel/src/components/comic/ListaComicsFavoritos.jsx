import Texto from "../common/Texto";
import { useState, useEffect } from "react";


const ListaComicsFavoritos = ({queryResult}) => {

    const [comicsFavoritos, setComicsFavoritos] = useState([]);

    useEffect(() => {

        const favoritos = [];
        console.log("hola");
      
        queryResult.forEach((comic) => {

            const comicFavorito = localStorage.getItem(comic.title);
            console.log("hola");
                        
            if (comicFavorito === 'like') {

                favoritos.push(comic.title); 
                console.log(comic.title);

            }

        });
      
        setComicsFavoritos((prevItems) => {

            return [...new Set([...prevItems, ...favoritos])];

        });

        console.log(comicsFavoritos);


    }, []); 

    return(

        <>

            {comicsFavoritos.map((tituloComic) => (

                <Texto key={tituloComic} contenido={tituloComic} classNameContainer="titulo-comic-list-favorite-comics" applyUsableText={false}></Texto>

            ))}

        </>     

    )

}

export default ListaComicsFavoritos;