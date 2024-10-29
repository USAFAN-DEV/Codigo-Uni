const privateKey = "03c4751f9d2e5109746a25ca450d09d2a72e4f67";
const baseURL = "https://gateway.marvel.com"
import CryptoJS from 'crypto-js';   


const getEndpointString = (ts, publicKey) => {

    const hash = CryptoJS.MD5(`${ts}${privateKey}${publicKey}`).toString();
    const endpointString = `?ts=${ts}&apikey=${publicKey}&hash=${hash}`;

    return endpointString;

}

export const getApiRequest = (request, publicKey) => {

    const apiRequest = (`${baseURL}${request}${getEndpointString(new Date().getTime(), publicKey)}`);
    return apiRequest;

}

