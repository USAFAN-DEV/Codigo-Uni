
const Imagen = ({src, alt, classNameContainer}) => {

    return(

        <div className={classNameContainer}>
            <img src={src} alt={alt}/>
        </div>

    )

}

export default Imagen;