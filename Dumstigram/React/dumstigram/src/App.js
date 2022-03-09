import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Post from './Post.js';

function App() {
  const [posts, setPosts] = useState([
    {
      id: '123',
      username: 'test1',
      avatarUrl: 'https://i.redd.it/b67mzvcj3fl81.jpg',
      caption: 'nice1',
      imgUrl: 'https://preview.redd.it/307v6axqh3l81.jpg?width=640&crop=smart&auto=webp&s=b01c842f82a0ad6cde6b24e19b26d8c8281aaa79',
    },
    {
      id: 'abc',
      username: 'test2',
      avatarUrl: 'https://preview.redd.it/307v6axqh3l81.jpg?width=640&crop=smart&auto=webp&s=b01c842f82a0ad6cde6b24e19b26d8c8281aaa79',
      caption: 'nice2',
      imgUrl: 'https://i.redd.it/b67mzvcj3fl81.jpg',
    },
  ]);

  useEffect(() => {
    console.log('ran useEffect');
    // Get posts from backend
    // postsResp = getPosts();
    axios({
        url: 'https://i.redd.it/j6a5ve7jtxl81.jpg', //your url
        method: 'GET',
        responseType: 'blob', // important
    }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        console.log(url);
        const postsResp = [
          {
            id: 'abc',
            post: {
              username: 'testaxios',
              avatarUrl: 'https://preview.redd.it/307v6axqh3l81.jpg?width=640&crop=smart&auto=webp&s=b01c842f82a0ad6cde6b24e19b26d8c8281aaa79',
              caption: 'niceaxios',
              imgUrl: url,
            }
          }
        ];
        setPosts(postsResp.map( resp => ({
          id: resp.id,
          post: resp.post,
        })));
    });
  }, []);

  return (
    <div className="app">
      <div className="app__header">
        <img
          className="app_headerImage"
          src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png"
          alt=""
        />
      </div>
      {
        posts.map((id, post) => {
          return <Post username={post.username} avatarUrl={post.avatarUrl} imgUrl={post.imgUrl} caption={post.caption} />
        })
      }
      {/* HEADER */}
      {/* POST */}
      {/* POST */}
      {/* POST */}
      {/* POST */}
      {/* POST */}
      {/* POST */}
    </div>
  );
}

export default App;
