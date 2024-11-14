
const getUsableText = (text) => {

    if(text.length > 25){

        return `${text.substring(0, 22)}...`.toUpperCase();

    } 

    return text.toUpperCase();

}


const Texto = ({contenido, classNameContainer, applyUsableText = true}) => {

    const newContenido = applyUsableText ? getUsableText(contenido) : contenido;

    return (

        <div className={classNameContainer}>

            <h1>{newContenido}</h1>

        </div>

    )
     
}

export default Texto;