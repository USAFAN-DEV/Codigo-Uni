import NavBar from './components/layouts/NavBar/NavBar.jsx'
import RecentComics from './components/comic/RecentComics/RecentComics.jsx'
import Background from './components/layouts/Background.jsx'


function App() {

  return (
    <>
      <Background classNameContainer="background"></Background>

      <NavBar></NavBar>

      <RecentComics></RecentComics>

    </>
  )
}

export default App
