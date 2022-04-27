import React, { useState, useEffect } from 'react';
import { Rings } from 'react-loader-spinner';
import { useCookies } from 'react-cookie';
import './styles/App.css';
import Post from './post/Post';
import Header from './header/Header';
import CreatePostModal from './post/CreatePostModal';
import * as api from './api';

function App() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState([false]);
  const [isCreatingPost, setIsCreatingPost] = useState([false]);
  const [cookies, setCookie] = useCookies(['user']);
  const [username, setUsername] = useState('PaPaBl3SsS');
  const [avatarUrl, setAvatarUrl] = useState('https://i.kym-cdn.com/photos/images/newsfeed/001/931/171/1d5.jpg');

  const getRecents = () => {
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
          console.log(l);
          const lCreated = parseInt(l.post.created, 10);
          const rCreated = parseInt(r.post.created, 10);
          return rCreated - lCreated;
        }));
        setIsLoading(false);
      })
      .catch(() => {
        setIsLoading(false);
      });
  };

  useEffect(() => {
    getRecents();
    setUsername(cookies.username)
    setUsername(cookies.avatarUrl)
  }, []);

  const updateUsername = (newUsername) => {
    setCookie('username', newUsername, { path: '/' });
  };

  const updateAvatarUrl = (newAvatarUrl) => {
    setCookie('avatarUrl', newAvatarUrl, { path: '/' });
  };

  const handleLogin = (newLoginUsername, newLoginAvatarUrl) => {
    updateUsername(username);
    updateAvatarUrl(avatarUrl);
    console.log(JSON.stringify(cookies));
    console.log(username);
    console.log(avatarUrl);
    setUsername(cookies.username);
    setAvatarUrl(cookies.avatarUrl);
    window.location.reload(0);
  };
  const handleOverlayClick = () => {
    setIsCreatingPost(!isCreatingPost);
  };

  return (
    <div className="app">
      <CreatePostModal
        key='createPostModal'
        creatingPost={isCreatingPost}
        closeModal={handleOverlayClick}
        avatarUrl={avatarUrl}
        username={username}
        triggerRefresh={getRecents}
      />
      <Header
        overlayClick={handleOverlayClick}
        avatarUrl={cookies.avatarUrl}
        username={cookies.username}
        setUsername={setUsername}
        setAvatarUrl={setAvatarUrl}
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
                  postId={key}
                  username={post.username}
                  avatarUrl={post.avatar_url}
                  imgUrl={post.img_url}
                  caption={post.caption}
                  expiration={post.expiration}
                  triggerRefresh={getRecents}
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
