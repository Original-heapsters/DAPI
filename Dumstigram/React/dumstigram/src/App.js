import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Post from './Post.js';

function App() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios({
        url: `${process.env.REACT_APP_BACKEND_SERVER}/recent/5`,
        method: 'GET',
        headers: {}
    }).then((response) => {
      const recentPosts = Object.keys(response.data).map((recent) => {
        const srcValue = "data:image/png;base64," + response.data[recent].split('\'')[1];
        return {
          id: recent,
          post: {
            username: recent,
            avatarUrl: 'https://image-cdn.hypb.st/https%3A%2F%2Fhypebeast.com%2Fimage%2F2020%2F06%2Fcolumbus-ohio-renamed-to-flavortown-petition-guy-fieri-tw.jpg?w=960&cbr=1&q=90&fit=max',
            caption: 'Toooasttyyyyyfffdfgdfsdfggggdfggggsdfsdfsd',
            imgUrl: srcValue,
          }
        };
      });
      setPosts(recentPosts.map( resp => ({
        key: resp.id,
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
      <div className="app__posts">
        <div className="app__postsLeft">
          {
            posts.map(({key, post}) => {
              return <Post key={key} username={post.username} avatarUrl={post.avatarUrl} imgUrl={post.imgUrl} caption={post.caption} />
            })
          }
        </div>
        <div className="app__postsright">

        </div>
      </div>
    </div>
  );
}

export default App;
