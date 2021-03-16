import React, { Fragment, useState } from "react";
import { Button, Form } from 'semantic-ui-react'


export const BookForm = ({request}) => {
  const [ISBN, setISBN] = useState("") 
  const [id, setId] = useState("")
  const [author_name, setAuthor] = useState("") 
  const [name, setName] = useState("")
  const [url, setUrl] = useState("")
  const [image_url, setImageUrl] = useState("")
  const [author_url, setAuthorUrl] = useState("") 
  const [book_rating, setRating] = useState("") 
  const [rating_count, setRatingCount] = useState("") 
  const [review_count, setReviewCount] = useState("") 
  const [similar_books, setSimilarBooks] = useState("") 
  const [text, setText] = useState("")
  const [books, setBooks] = useState([])
  

  const handleTextChange = e => {
    setText(e.target.value)
  }

  const handleUpdateClick = async e => {
    const data = {ISBN, author_name, author_url, id, image_url, name, book_rating, rating_count, review_count, similar_books, url}
    console.log(data)
    const api_url = "http://127.0.0.1:5000/api/book?id=" + text
    await fetch(api_url, {
      method:'PUT',
      headers : { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'},
      body: JSON.stringify(data)
    })
    .then((response) => {
    if(!response.ok) throw new Error(response.status);
    else alert("The PUT request is successful!")
    })
  }

  const handleBookInfo = async e => {
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
    setName(data[0].name)
    setAuthor(data[0].author_name)
    setISBN(data[0].ISBN)
    setId(data[0].id)
    setRating(data[0].rating)
    setRatingCount(data[0].rating_count)
    setReviewCount(data[0].review_count)
    setUrl(data[0].url)
    setImageUrl(data[0].image_url)
    setAuthorUrl(data[0].author_url)
    setSimilarBooks(data[0].similar_books)
    })
  }

  const handleSubmitClick = async e => {
    const book = {ISBN, author_name, author_url, id, image_url, name, book_rating, rating_count, review_count, url, similar_books}
    console.log(book)
    const api_url = "http://127.0.0.1:5000/api/book"
    await fetch(api_url, {
      method:'POST',
      headers : { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'},
      body: JSON.stringify(book)
    })
    .then((response) => {
    if(!response.ok) throw new Error(response.status);
    else alert("The POST request is successful!")
    })
  }

  return (
    <div>
    {request === 'PUT' &&
    <div>
        <label>
          Please enter the bood id:
          <input type="text" value={text} onChange={handleTextChange} />
        </label>
        <input onClick={handleBookInfo} type="submit" value="Submit" />
      </div>}

    {(request === 'PUT' && books[0]) && 
    <Form>
      <Form.Group>
      <Form.Input label='Book Name' value={name} placeholder='Book Name' width={6} onChange={e => setName(e.target.value)}/>
      <Form.Input label='Author' value={author_name} value={author_name} placeholder='Author' width={4} onChange={e => setAuthor(e.target.value)}/>
      <Form.Input label='ISBN' value={ISBN} placeholder='ISBN' value={ISBN} width={6} onChange={e => setISBN(e.target.value)}/>
    </Form.Group>
    <Form.Group>
      <Form.Input label='Book id' value={id} placeholder='id' onChange={e => setId(e.target.value)} width={4} />
      <Form.Input label='Rating' value={book_rating} placeholder='Rating' width={4} onChange={e => setRating(e.target.value)}/>
      <Form.Input label='Rating Count' value={rating_count} placeholder='Rating Count' width={4} onChange={e => setRatingCount(e.target.value)}/>
      <Form.Input label='Review Count' value={review_count} placeholder='Review Count' width={4} onChange={e => setReviewCount(e.target.value)}/>
    </Form.Group>
      <Form.Input label='Book url' value={url} placeholder='Book url' width={18} onChange={e => setUrl(e.target.value)}/>
      <Form.Input label='Image url' value={image_url} placeholder='Image url' width={18} onChange={e => setImageUrl(e.target.value)}/>
      <Form.Input label='Author url' value={author_url} placeholder='Author url' width={18} onChange={e => setAuthorUrl(e.target.value)}/>
      <Form.Input label='Similar Books' value={similar_books} placeholder='Similar Books' onChange={e => setSimilarBooks(e.target.value)} width={25} />
    <Form.Field>
      <br></br>
      <Button primary onClick={handleUpdateClick}>Update</Button>
    </Form.Field>
  </Form>}
    
  {request === 'POST' && 
    <Form>
    <Form.Group>
      <Form.Input label='Book Name' value={name} placeholder='Book Name' width={6} onChange={e => setName(e.target.value)}/>
      <Form.Input label='Author' value={author_name} placeholder='Author' width={4} onChange={e => setAuthor(e.target.value)}/>
      <Form.Input label='ISBN' value={ISBN} placeholder='ISBN' width={6} onChange={e => setISBN(e.target.value)}/>
    </Form.Group>
    <Form.Group>
      <Form.Input label='Book id' value={id} placeholder='id' onChange={e => setId(e.target.value)} width={4} />
      <Form.Input label='Rating' value={book_rating} placeholder='Rating' width={4} onChange={e => setRating(e.target.value)}/>
      <Form.Input label='Rating Count' value={rating_count} placeholder='Rating Count' width={4} onChange={e => setRatingCount(e.target.value)}/>
      <Form.Input label='Review Count' value={review_count} placeholder='Review Count' width={4} onChange={e => setReviewCount(e.target.value)}/>
    </Form.Group>
      <Form.Input label='Book url' value={url} placeholder='Book url' width={18} onChange={e => setUrl(e.target.value)}/>
      <Form.Input label='Image url' value={image_url} placeholder='Image url' width={18} onChange={e => setImageUrl(e.target.value)}/>
      <Form.Input label='Author url' value={author_url} placeholder='Author url' width={18} onChange={e => setAuthorUrl(e.target.value)}/>
      <Form.Input label='Similar Books' value={similar_books} placeholder='Similar Books' onChange={e => setSimilarBooks(e.target.value)} width={25} />
    <Form.Field>
      <br></br>
      <Button primary onClick={handleSubmitClick}>Submit</Button>
    </Form.Field>
  </Form>}


    
  </div>
  );
};