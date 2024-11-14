import Favorito from '../../assets/heart.png';
import FavoritoRojo from '../../assets/redHeart.png';
import { useState, useEffect } from 'react';

const ImagenLike = ({ classNameContainer, clave, tituloComicCorrespondiente, onFavoriteChange }) => {
    
    const [isLiked, setIsLiked] = useState(false); //Estado para guardar si el es like o no like

    //Para mostrar los corazones rojos guardados en el localStorage. Se ejecuta al renderizar el componente
    useEffect(() => {

        const status = localStorage.getItem(clave);

        if (status === 'like') {

            setIsLiked(true); 

        }

    }, []);

    const handleLikeClick = () => {

        const newStatus = !isLiked;
        setIsLiked(newStatus);

        if (newStatus) { //Es like

            localStorage.setItem(clave, 'like'); 
            onFavoriteChange(tituloComicCorrespondiente, true);

        } 
        else { //Es dislike

            // Si se desmarcó como favorito
            localStorage.removeItem(clave);
            onFavoriteChange(tituloComicCorrespondiente, false);

        }
    };

    return (

        <div className={classNameContainer}>

            <img onClick={handleLikeClick} src={isLiked ? FavoritoRojo : Favorito} alt="corazonFoto"/>

        </div>
    );
};

export default ImagenLike;
