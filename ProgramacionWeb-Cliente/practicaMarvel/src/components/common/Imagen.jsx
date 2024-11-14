
const Imagen = ({src, alt, classNameContainer, onClick = () => {}}) => {

    return(

        <div className={classNameContainer}>
            <img onClick={()=>onClick(src)} src={src} alt={alt}/>
        </div>

    )

}

export default Imagen;