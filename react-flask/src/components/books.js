import React from 'react';

export const Books = ( {books} ) => {
  return (
    <ul>
      {books.map(function(book, index){
        return (
          <div>
          <h3>Book {index}</h3>
          <ul>
        <img src={book.image_url} width="200" height="300"/>
        <li key='isbn'>ISBN: {book.ISBN}</li>
        <li key='name'>Book Title: <a href={book.url}>{book.name}</a></li>
        <li key='author'>Author: <a href={book.author_url}>{book.author_name}</a></li>
        <li key='rating'>Rating: {book.rating} (There are {book.rating_number} ratings in total</li>
        <li key='review'>Review number: {book.review_count}</li>
        <li key='similar_author'>Similar books: {book.similar_books}</li>
        </ul>
        </div>
        );
      })}
    </ul>
  );
};

