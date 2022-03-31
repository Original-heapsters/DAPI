import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Rings } from  'react-loader-spinner'
import './App.css';
import Post from './Post.js';
import Header from './Header.js';
import CreatePostOverlay from './CreatePostOverlay.js'

function App() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState([false]);
  const [username] = useState('PaPaBl3Ss');
  const [avatarUrl] = useState('https://i.redd.it/b67mzvcj3fl81.jpg');

  useEffect(() => {
    setIsLoading(true);
    axios({
        url: `${process.env.REACT_APP_BACKEND_SERVER}/recent/5`,
        method: 'GET',
        headers: {}
    }).then((response) => {
      const recentPosts = Object.keys(response.data).map((recent) => {
        const post = response.data[recent];
        return {
          id: recent,
          post: {
            ...post,
            img_url: `${process.env.REACT_APP_BACKEND_SERVER}${post['img_url'].substr(1)}`,
          }
        };
      });
      setPosts(recentPosts.map( resp => ({
        key: resp.id,
        post: resp.post,
      })).sort((l, r) => {
        const lCreated = parseInt(l.post.created);
        const rCreated = parseInt(r.post.created);
        return rCreated - lCreated;

      }));
      setIsLoading(false);
    })
    .catch((error) => {
      console.log(error);
      setIsLoading(false);
    });
  }, []);

  const [isCreatingPost, setIsCreatingPost] = useState([false])

	const handleOverlayClick = () => {
		console.log('clicked the thing')
		setIsCreatingPost(!isCreatingPost)
	}

  return (
    <div className="app">
      <CreatePostOverlay creatingPost={isCreatingPost} overlayClick={handleOverlayClick} avatarUrl={avatarUrl} username={username}/>
      <Header overlayClick={handleOverlayClick} avatarUrl={avatarUrl} username={username}/>
      <div className="app__posts">
        { isLoading
          ?<Rings color="#00BFFF" height={50} width={50} />
          :<div className="app__postsLeft">
            {
              posts.map(({key, post}) => {
                return <Post key={key} username={post.username} avatarUrl={post.avatar_url} imgUrl={post.img_url} caption={post.caption} expiration={post.expiration} />
              })
            }
          </div>
        }
        <div className="app__postsright">
        </div>
      </div>
    </div>
  );
}

export default App;
