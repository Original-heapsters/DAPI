import React, { useState, useEffect } from 'react';
import { Rings } from 'react-loader-spinner';
import { useCookies } from 'react-cookie';
import './styles/App.css';
import Post from './post/Post';
import Header from './header/Header';
import CreatePostOverlay from './post/CreatePostOverlay';
import * as api from './api';

function App() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState([false]);
  const [isCreatingPost, setIsCreatingPost] = useState([false]);
  const [cookies, setCookie] = useCookies(['user']);
  const [username, setUsername] = useState('PaPaBl3SsS');
  const [avatarUrl, setAvatar] = useState('https://i.kym-cdn.com/photos/images/newsfeed/001/931/171/1d5.jpg');

  useEffect(() => {
    setIsLoading(true);
    async function fetchData() {
      const response = await api.getRecentFeed(5);
      return response;
    }
    fetchData()
      .then((recentPosts) => {
        setPosts(recentPosts.map((resp) => ({
          key: resp.id,
          post: resp.post,
        })).sort((l, r) => {
          const lCreated = parseInt(l.post.created, 10);
          const rCreated = parseInt(r.post.created, 10);
          return rCreated - lCreated;
        }));
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  }, []);

  const updateUsername = (newUsername) => {
    setCookie('username', newUsername, { path: '/' });
  };

  const updateAvatarUrl = (newAvatarUrl) => {
    setCookie('avatarUrl', newAvatarUrl, { path: '/' });
  };

  const handleLogin = (newLoginUsername, newLoginAvatarUrl) => {
    updateUsername(newLoginUsername);
    updateAvatarUrl(newLoginAvatarUrl);
    setUsername(cookies.username);
    setAvatar(cookies.avatarUrl);
  };
  const handleOverlayClick = () => {
    setIsCreatingPost(!isCreatingPost);
  };

  return (
    <div className="app">
      <CreatePostOverlay
        creatingPost={isCreatingPost}
        overlayClick={handleOverlayClick}
        avatarUrl={avatarUrl}
        username={username}
      />
      <Header
        overlayClick={handleOverlayClick}
        avatarUrl={cookies.avatarUrl}
        username={cookies.username}
        triggerLogin={handleLogin}
      />
      <div className="app__posts">
        { isLoading
          ? <Rings color="#00BFFF" height={50} width={50} />
          : (
            <div className="app__postsLeft">
              {
              posts.map(({ key, post }) => (
                <Post
                  key={key}
                  username={post.username}
                  avatarUrl={post.avatar_url}
                  imgUrl={post.img_url}
                  caption={post.caption}
                  expiration={post.expiration}
                />
              ))
            }
            </div>
          )}
        <div className="app__postsright" />
      </div>
    </div>
  );
}

export default App;
