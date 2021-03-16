import React, {useState} from 'react';
import { Books } from "./Books";

const RankBookPage = () => {
    const [text, setText] = useState("")
    const [books, setBooks] = useState([])


    const handleTextChange = e => {
        setText(e.target.value)
    }

    const handleSubmit = async e => {
        e.preventDefault()
        const url = "http://127.0.0.1:5000/api/books"
        await fetch(url, {
                method:'GET',
                headers : { 
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                }})
        .then((response) => {
            if(!response.ok) throw new Error(response.status);
            else {
            alert("The GET request is successful!")
            return response.json();}
        })
        .then((data) => {
            setBooks(data.slice(0, text))
            console.log(data)
        })
    }


    return (
        <div>
            <form onSubmit={handleSubmit}>
            <label>
            Please enter k (the ranking of top k highest rated books):
            <input type="text" value={text} onChange={handleTextChange} />
            </label>
            <input type="submit" value="Submit" />
            </form>
            
            <Books books={books}/>
        </div>
    );
};

export default RankBookPage;