import { useState } from 'react'
import Footer from './components/layouts/Footer.jsx'
import NavBar from './components/layouts/NavBar/NavBar.jsx'
import RecentComics from './components/comic/RecentComics/RecentComics.jsx'
import Background from './components/Background.jsx'


function App() {

  return (
    <>
      <Background></Background>

      <NavBar></NavBar>

      <RecentComics></RecentComics>

      <Footer></Footer>
    </>
  )
}

export default App
