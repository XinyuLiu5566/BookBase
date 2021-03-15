import './App.css';
import React, { useEffect, useState } from "react";
import Select from 'react-select'
import { Books } from "./components/Books";
import { Authors } from "./components/Authors";
import { BookForm } from "./components/BookForm";
import { Button } from 'semantic-ui-react';
import { AuthorForm } from './components/AuthorForm';


function App() {
  const [books, setBooks] = useState([])
  const [authors, setAuthors] = useState([])
  const [way, setWay] = useState("")
  const [request, setRequest] = useState("")
  const [text, setText] = useState("")
  const [bookShow, setBookShow] = useState(false)
  const [authorShow, setAuthorShow] = useState(false)
  const [putAttr, setPutAttr] = useState("")
  const [postAttr, setPostAttr] = useState("")



  const options = [
    { value: 'book_id', label: 'Book Id' },
    { value: 'author_id', label: 'Author Id' },
    { value: 'search_query', label: 'Search Query' }
  ]
  const put_options = [
    { value: 'book_id', label: 'Book Id' },
    { value: 'author_id', label: 'Author Id' },
  ]

  const post_options = [
    { value: 'book', label: 'Book' },
    { value: 'author', label: 'Author' },
  ]


  const request_options = [
    { value: 'PUT', label: 'PUT' },
    { value: 'GET', label: 'GET' },
    { value: 'POST', label: 'POST' },
    { value: 'DELETE', label: 'DELETE' }
  ]


  const handleWayChange = e => {
    setWay(e.value);
  }

  const handlePut = e => {
    setPutAttr(e.value)
  }

  const handlePost = e => {
    setPostAttr(e.value)
  }


  const handleRequestChange = e => {
    setWay("")
    setPutAttr("")
    setRequest(e.value);
  }

  const handleTextChange = e => {
    setText(e.target.value)
  }

  const handleBookSubmit = async e => {
    e.preventDefault()
    if (request === "GET") {
      setBookShow(true)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book?id=" + text
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
        setBooks(data)
        console.log(books)
      })
    } else if (request === "DELETE") {
      setBookShow(false)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book?id=" + text
      await fetch(url, {
        method:'DELETE',
        headers : { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
       }})
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else {
          alert("The DELETE request is successful!")
        }
      })
    } else if (request === "DELETE") {
      setBookShow(false)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book?id=" + text
      await fetch(url, {
        method:'DELETE',
        headers : { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
       }})
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else {
          alert("The DELETE request is successful!")
        }
      })
    } else if (request === "DELETE") {
      setBookShow(false)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book?id=" + text
      await fetch(url, {
        method:'DELETE',
        headers : { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
       }})
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else {
          alert("The DELETE request is successful!")
        }
      })
    }
  }

  const handleAuthorSubmit = async e => {
    e.preventDefault()
    if (request === "GET") {
      setBookShow(false)
      setAuthorShow(true)
      const url = "http://127.0.0.1:5000/api/author?id=" + text
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
        setAuthors(data)
        console.log(authors);
      })
    } else if (request === "DELETE") {
      setBookShow(false)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book?id=" + text
      await fetch(url, {
        method:'DELETE',
        headers : { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
       }})
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else {
          alert("The GET request is successful!")
        }
      })
    } else if (request === "PUT") {
      setBookShow(false)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book?id=" + text
      await fetch(url, {
        method:'DELETE',
        headers : { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
       }})
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else {
          alert("The GET request is successful!")
        }
      })
    } else if (request === "POST") {
      setBookShow(false)
      setAuthorShow(false)
      const url = "http://127.0.0.1:5000/api/book"
      await fetch(url, {
        method:'DELETE',
        headers : { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
       }})
      .then((response) => {
        if(!response.ok) throw new Error(response.status);
        else {
          alert("The GET request is successful!")
        }
      })
    }
  }


  const handleQuerySubmit = e => {
    e.preventDefault()
    if (request === "GET") {
      if (text.includes('author')) {
        console.log("it is author")
        setBookShow(false)
        setAuthors(true)
        const url = "http://127.0.0.1:5000/api/search?q=" + text
        fetch(url, {
              method:'GET',
              headers : { 
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
            }}).then(response =>
            response.json().then(data => {
              setAuthors(data);
              console.log(authors)
          })
        );
      } else if (text.includes('book')) {
        console.log("it is a book")
        setBookShow(true)
        setAuthors(false)
        const url = "http://127.0.0.1:5000/api/search?q=" + text
        fetch(url, {
              method:'GET',
              headers : { 
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': '*',
            }}).then(response =>
            response.json().then(data => {
              setBooks(data);
              console.log(books)
          })
        );
      }
    }
  }

  return (
    <div className = "container">
        <h1>Please select the way you like to get your data</h1>
        <Select 
          placeholder="Select the request type"
          autosize={true}
          options = {request_options}
          value={options.find(obj => obj.value === request)}
          onChange={handleRequestChange}
        />
        {(request==='GET' || request==='DELETE') && <Select 
          placeholder="Select which attribute you wanna search"
          autosize={true}
          options = {options}
          value={options.find(obj => obj.value === way)}
          onChange={handleWayChange}
        />}
        {(request==='PUT') && <Select 
          placeholder="Select which attribute you wanna search"
          autosize={true}
          options = {put_options}
          value={put_options.find(obj => obj.value === putAttr)}
          onChange={handlePut}
        />}

        {(request==='POST') && <Select 
          placeholder="Select which you want to POST (book/author)"
          autosize={true}
          options = {post_options}
          value={post_options.find(obj => obj.value === postAttr)}
          onChange={handlePost}
        />} 

        <br></br>

        {(request === 'PUT' && putAttr === 'book_id') && <BookForm request = {request}/>}
        {(request === 'PUT' && putAttr === 'author_id') && <AuthorForm request = {request}/>}
        {(request === 'POST' && postAttr === 'book') && <BookForm request = {request}/>}
        {(request === 'POST' && postAttr === 'author') && <AuthorForm request = {request}/>}


        {(way === 'book_id') && <form onSubmit={handleBookSubmit}>
        <label>
          Please enter the bood id:
          <input type="text" value={text} onChange={handleTextChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>}

        {way === 'author_id' && <form onSubmit={handleAuthorSubmit}>
        <label>
          Please enter the author id:
          <input type="text" value={text} onChange={handleTextChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>}

        {way === 'search_query' && <form onSubmit={handleQuerySubmit}>
        <label>
          Please enter the query:
          <input type="text" value={text} onChange={handleTextChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>}


        {bookShow === true && <Books books={books} />}
        {authorShow === true && <Authors authors={authors} />}
  
    </div>
  );
}

export default App;
