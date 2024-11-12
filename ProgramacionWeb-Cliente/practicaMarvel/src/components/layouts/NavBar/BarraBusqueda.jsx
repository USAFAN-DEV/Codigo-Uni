import Boton from '../../common/Boton.jsx'
import Imagen from '../../common/Imagen.jsx';

import lupa from '../../../assets/search-symbol.png'

const BarraBusqueda = () => {

    return(

            <form id="barra-busqueda">

                <input id="input-barra-busqueda" type="text" placeholder="Buscar comic"></input>
                <Boton buttonType={"submit"} classNameContainer={"boton-container"}>

                    <Imagen src={lupa} alt={"fotoLupa"} classNameContainer={'icon-container'}></Imagen>

                </Boton>

            </form>

    )

}

export default BarraBusqueda;