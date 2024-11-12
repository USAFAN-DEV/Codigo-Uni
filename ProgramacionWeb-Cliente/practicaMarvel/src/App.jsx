import { useState } from 'react'
import Footer from './components/layouts/Footer.jsx'
import NavBar from './components/layouts/NavBar/NavBar.jsx'
import RecentComics from './components/comic/RecentComics/RecentComics.jsx'


function App() {

  return (
    <>
      <NavBar></NavBar>

      <RecentComics></RecentComics>

      <Footer></Footer>
    </>
  )
}

export default App
