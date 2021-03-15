import React, { useState } from "react";
import { Button, Form } from 'semantic-ui-react'


export const AuthorForm = ({request}) => {
    const [author_name, setAuthorName] = useState("")
    const [author_url, setAuthorUrl] = useState("") 
    const [author_id, setId] = useState("")
    const [author_rating, setRating] = useState("") 
    const [rating_count, setRatingCount] = useState("")
    const [review_count, setReviewCount] = useState("")
    const [author_image_url, setAuthorImageUrl] = useState("")
    const [related_author, setRelatedAuthor] = useState("") 
    const [author_book, setAuthorBook] = useState("") 
    const [text, setText] = useState("")
    const [authors, setAuthors] = useState([])
  

  const handleTextChange = e => {
    setText(e.target.value)
  }

  const handleUpdateClick = async e => {
    const data = {author_name, author_url, author_id, author_rating, rating_count, review_count, author_image_url, related_author, author_book}
    console.log(data)
    const api_url = "http://127.0.0.1:5000/api/author?id=" + text
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

  const handleAuthorInfo = async e => {
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
    setAuthorName(data[0].name)
    setAuthorUrl(data[0].url)
    setId(data[0].id)
    setRating(data[0].rating)
    setRatingCount(data[0].rating_count)
    setReviewCount(data[0].review_count)
    setAuthorImageUrl(data[0].image_url)
    setRelatedAuthor(data[0].related_author)
    setAuthorBook(data[0].author_books)
    })
  }

  const handleSubmitClick = async e => {
    const data = {author_name, author_url, author_id, author_rating, rating_count, review_count, author_image_url, related_author, author_book}
    console.log(data)
    const api_url = "http://127.0.0.1:5000/api/author"
    await fetch(api_url, {
      method:'POST',
      headers : { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'},
      body: JSON.stringify(data)
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
          Please enter the author id:
          <input type="text" value={text} onChange={handleTextChange} />
        </label>
        <input onClick={handleAuthorInfo} type="submit" value="Submit" />
      </div>}

    {(request === 'PUT' && authors[0]) && 
    <Form>
      <Form.Group>
      <Form.Input label='Author Name' value={author_name} placeholder='Author Name' width={6} onChange={e => setAuthorName(e.target.value)}/>
      <Form.Input label='Author Id' value={author_id} placeholder='Author Id' width={4} onChange={e => setId(e.target.value)}/>
    </Form.Group>
    <Form.Group>
      <Form.Input label='Rating' value={author_rating} placeholder='Rating' width={4} onChange={e => setRating(e.target.value)}/>
      <Form.Input label='Rating Count' value={rating_count} placeholder='Rating Count' width={4} onChange={e => setRatingCount(e.target.value)}/>
      <Form.Input label='Review Count' value={review_count} placeholder='Review Count' width={4} onChange={e => setReviewCount(e.target.value)}/>
    </Form.Group>
      <Form.Input label='Author Books' value={author_book} placeholder='Author Books' width={18} onChange={e => setAuthorBook(e.target.value)}/>
      <Form.Input label='Image url' value={author_image_url} placeholder='Image url' width={18} onChange={e => setAuthorImageUrl(e.target.value)}/>
      <Form.Input label='Author url' value={author_url} placeholder='Author url' width={18} onChange={e => setAuthorUrl(e.target.value)}/>
      <Form.Input label='Related Author' value={related_author} placeholder='Related Author' onChange={e => setRelatedAuthor(e.target.value)} width={25} />
    <Form.Field>
      <br></br>
      <Button primary onClick={handleUpdateClick}>Update</Button>
    </Form.Field>
  </Form>}
    
  {request === 'POST' && 
    <Form>
    <Form.Group>
      <Form.Input label='Author Name' value={author_name} placeholder='Author Name' width={6} onChange={e => setAuthorName(e.target.value)}/>
      <Form.Input label='Author Id' value={author_id} placeholder='Author Id' width={4} onChange={e => setId(e.target.value)}/>
    </Form.Group>
    <Form.Group>
      <Form.Input label='Rating' value={author_rating} placeholder='Rating' width={4} onChange={e => setRating(e.target.value)}/>
      <Form.Input label='Rating Count' value={rating_count} placeholder='Rating Count' width={4} onChange={e => setRatingCount(e.target.value)}/>
      <Form.Input label='Review Count' value={review_count} placeholder='Review Count' width={4} onChange={e => setReviewCount(e.target.value)}/>
    </Form.Group>
      <Form.Input label='Author Books' value={author_book} placeholder='Author Books' width={18} onChange={e => setAuthorBook(e.target.value)}/>
      <Form.Input label='Image url' value={author_image_url} placeholder='Image url' width={18} onChange={e => setAuthorImageUrl(e.target.value)}/>
      <Form.Input label='Author url' value={author_url} placeholder='Author url' width={18} onChange={e => setAuthorUrl(e.target.value)}/>
      <Form.Input label='Related Author' value={related_author} placeholder='Related Author' onChange={e => setRelatedAuthor(e.target.value)} width={25} />
    <Form.Field>
      <br></br>
      <Button primary onClick={handleSubmitClick}>Submit</Button>
    </Form.Field>
  </Form>}


    
  </div>
  );
};