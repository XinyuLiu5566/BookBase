import React from 'react';

export const Authors = ( {authors} ) => {
  return (
    <ul>
      {authors.map(function(author, index){
        return (
          <div>
          <h3>Author {index}</h3>
          <ul>
        <img src={author.image_url} width="200" height="300"/>
        <li key='name'>Author Name: <a href={author.url}>{author.name}</a></li>
        <li key='rating'>Rating: {author.rating} (There are {author.rating_count} ratings in total</li>
        <li key='review'>Review number: {author.review_count}</li>
        <li key='related_author'>Related Authors: {author.related_author}</li>
        <li key='author_books'>Author Books: {author.author_books} </li>
        </ul>
        </div>
        );
      })}
    </ul>
  );
};