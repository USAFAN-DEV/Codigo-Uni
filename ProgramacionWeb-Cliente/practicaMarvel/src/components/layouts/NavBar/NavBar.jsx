//IMAGENES
import logo from  '../../../assets/logoBlanco.png'
import home from '../../../assets/home.png'
import favorito from '../../../assets/heart.png'

//COMPONENTESS
import Texto from '../../common/Texto.jsx'
import Imagen from '../../common/Imagen.jsx'
import BarraBusqueda from './BarraBusqueda.jsx'


const NavBar = () => {

    return(
        <>
            <nav>

                <Imagen src={logo} alt={"fotoLogo"} classNameContainer={"logo-container"}></Imagen>

                <BarraBusqueda></BarraBusqueda>

                <div id='menu-container'>

                    <a className="item-menu">

                        <Texto contenido={"HOME"} classNameContainer={"item-menu-texto-container"}></Texto>
                        <Imagen src={home} alt={"fotoHome"} classNameContainer={"item-menu-icon-container"}></Imagen>
                    
                    </a>

                    <a className="item-menu">

                        <Texto contenido={"FAVORITOS"} classNameContainer={"item-menu-texto-container"}></Texto>
                        <Imagen src={favorito} alt={"fotoLike"} classNameContainer={"item-menu-icon-container"}></Imagen>
                        
                    </a> 

                </div>
                   
            </nav>
            
            <div id="navBar-separador"></div>
        </>
    )
   

}

export default NavBar