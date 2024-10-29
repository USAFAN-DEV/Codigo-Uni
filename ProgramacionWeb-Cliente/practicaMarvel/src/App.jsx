import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {getApiRequest} from './utilities/apikey.js'

const PUBLIC_KEY = "5c9eca00013e6a51ac258f09402ebcd9";

function App() {

  const api_request = getApiRequest("/v1/public/characters", PUBLIC_KEY);
  console.log(api_request);

  return (
    <>
      <div>
        <h1>Marvel API Request</h1>
        <p>Generated API request URL:</p>
        <code>{api_request}</code>
      </div>
      
    </>
  )
}

export default App
