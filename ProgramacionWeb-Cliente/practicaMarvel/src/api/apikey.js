const PRIVATE_KEY = "03c4751f9d2e5109746a25ca450d09d2a72e4f67";
const PUBLIC_KEY = "5c9eca00013e6a51ac258f09402ebcd9";
const BASE_URL = "https://gateway.marvel.com"
import CryptoJS from 'crypto-js';   


const getEndpointString = (ts) => {

    const hash = CryptoJS.MD5(`${ts}${PRIVATE_KEY}${PUBLIC_KEY}`).toString();
    const endpointString = `ts=${ts}&apikey=${PUBLIC_KEY}&hash=${hash}`;

    return endpointString;

}

export const getApiRequest = (request) => {

    const apiRequest = (`${BASE_URL}${request}${getEndpointString(new Date().getTime(), PUBLIC_KEY)}`);

    console.log("Pidiendo query");
    
    return fetch(apiRequest).then(response => response.json());

    

}

