import Imagen from '../../common/Imagen.jsx'
import Texto from '../../common/Texto.jsx'

const SingleComic = (imagenComic, tituloComic) => {

    return(

        <div id="comic-container">
            
            <Imagen src={imagenComic} alt={`Foto de ${tituloComic}`} classNameContainer={"foto-comic-container"}></Imagen>
            <Texto contenido={tituloComic} classNameContainer={"titulo-comic-container"}></Texto>

        </div>

    )

}

export default SingleComic;