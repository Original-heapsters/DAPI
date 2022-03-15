import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Rings } from  'react-loader-spinner'
import './App.css';
import Post from './Post.js';
import Header from './Header.js';
// import uploadIcon from '/uploadIcon.svg';

function App() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState([false]);

  useEffect(() => {
    setIsLoading(true);
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
            caption: 'Toooasttyyyyy',
            imgUrl: srcValue,
          }
        };
      });
      setPosts(recentPosts.map( resp => ({
        key: resp.id,
        post: resp.post,
      })).sort((l, r) => {
        const lExpir = parseInt(l.key.substr(0, l.key.indexOf('-')));
        const rExpir = parseInt(r.key.substr(0, r.key.indexOf('-')));
        console.log(`lExpir is ${lExpir}`);
        console.log(`rExpir is ${rExpir}`);
        return rExpir - lExpir;

      }));
      setIsLoading(false);
    })
    .catch((error) => {
      console.log(error);
      setIsLoading(false);
    });
  }, []);

  return (
    <div className="app">
      <Header />
      <div className="app__posts">
        { isLoading
          ?<Rings color="#00BFFF" height={50} width={50} />
          :<div className="app__postsLeft">
            {
              posts.map(({key, post}) => {
                return <Post key={key} username={post.username} avatarUrl={post.avatarUrl} imgUrl={post.imgUrl} caption={post.caption} />
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
