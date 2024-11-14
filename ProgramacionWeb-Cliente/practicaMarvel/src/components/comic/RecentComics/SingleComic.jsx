import Imagen from '../../common/Imagen.jsx'
import Texto from '../../common/Texto.jsx'
import Close from '../../../assets/close.png'
import Background from '../../layouts/Background.jsx'
import { useRef } from 'react'
import { useEffect } from 'react'

/*
The ::backdrop pseudo-element is specific to the <dialog> element, but it only works if the dialog is opened using the native <dialog> methods like showModal() or show()
*/ 

const SingleComic = ({mostrarDialog, imagenComic, tituloComic, descripcionComic, personajes, cerrarDialog}) => {

    const dialogRef = useRef(null);

    useEffect(() => {
        const dialog = dialogRef.current;

        if (mostrarDialog) {
            dialog.showModal(); 
        } else {
            dialog.close(); 
        }
    }, [mostrarDialog]);

    return(

        <dialog id="comic-container" ref={dialogRef}>

            <Background classNameContainer="background2"></Background>

            <div id="comic-info">

                <Imagen src={Close} alt={"Cerrar"} classNameContainer={"boton-cerrar-container"} onClick={cerrarDialog}></Imagen>

                <Imagen src={imagenComic} alt={`Foto de ${tituloComic}`} classNameContainer={"foto-comic-info"}></Imagen>

                <div id="comic-text">

                    <Texto applyUsableText={false} contenido={tituloComic} classNameContainer={"titulo-comic-text"}></Texto>
                    <Texto applyUsableText={false} contenido={descripcionComic} classNameContainer={"descripcion-comic-text"}></Texto>

                </div>

            </div>

            <Texto contenido={"PERSONAJES"} classNameContainer={"titulo-personajes-container"}></Texto>

            <div id="personajes-container">

                {Object.entries(personajes).map(([nombrePersonaje, fotoPersonaje]) => ( //Object.entries(diccionario) devuelve un array de pares [clave, valor]

                    <div key={nombrePersonaje} className="personaje-container">

                        <Imagen alt="fotoPersonaje" src={fotoPersonaje} classNameContainer="imagen-personaje-container"></Imagen> 
                        <Texto contenido={nombrePersonaje} classNameContainer="nombre-personaje-container" applyUsableText={false}></Texto>

                    </div>

                ))}

            </div>

        </dialog>

    )

}

export default SingleComic;