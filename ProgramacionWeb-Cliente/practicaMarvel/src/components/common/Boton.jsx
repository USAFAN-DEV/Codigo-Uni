
const Boton = ({buttonType, classNameContainer, children}) => {

    return(

        <div className={classNameContainer}>

            <button type={buttonType}>{children}</button>

        </div>

    )

}

export default Boton;