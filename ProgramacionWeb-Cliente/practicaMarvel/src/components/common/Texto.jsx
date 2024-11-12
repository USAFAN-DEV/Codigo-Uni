
const getUsableText = (text) => {

    if(text.length > 25){

        return `${text.substring(0, 22)}...`.toUpperCase();

    } 

    return text.toUpperCase();

}


const Texto = ({contenido, classNameContainer}) => {

    return(

        <div className={classNameContainer}>

            <h1>{getUsableText(contenido)}</h1>
            
        </div>

    )

}

export default Texto;