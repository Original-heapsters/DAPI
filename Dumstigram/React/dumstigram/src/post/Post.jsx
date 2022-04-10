import '../styles/Post.css';
import React, { useState, useEffect } from 'react';
import { Rings } from 'react-loader-spinner';
import Avatar from '@material-ui/core/Avatar';
import * as api from '../api';

function Post({
  postId = '123',
  username = 'username',
  avatarUrl = 'https://i.redd.it/b67mzvcj3fl81.jpg',
  caption = 'lorem ipsum',
  imgUrl = 'https://i.redd.it/j6a5ve7jtxl81.jpg',
  expiration = 420,
  triggerRefresh,
}) {
  const [timeLeft, setTimeLeft] = useState(expiration);
  const [formattedTimeLeft, setFormattedTimeLeft] = useState(0);
  const [isRefrying, setIsRefrying] = useState(false);

  const calculateTimeLeft = () => {
    const newTimeLeft = timeLeft - 1;
    const expireTime = new Date(0);
    expireTime.setSeconds(newTimeLeft);
    setTimeLeft(newTimeLeft);
    return expireTime;
  };

  const handleRefry = () => {
    setIsRefrying(true);
    const formData = new FormData();

    formData.append('username', username);
    formData.append('caption', caption);
    formData.append('ttl', expiration);
    formData.append('avatar', avatarUrl);
    async function refry(postInfoId, postInfo) {
      await api.refryPost(postInfoId, postInfo);
    }

    refry(postId, formData)
      .then(() => {
        triggerRefresh();
        setIsRefrying(false);
      })
      .catch(() => {
        triggerRefresh();
        setIsRefrying(false);
      });
  };

  useEffect(() => {
    setTimeout(() => {
      const expireTime = calculateTimeLeft();
      setFormattedTimeLeft(expireTime.toISOString().substr(11, 8));
    }, 1000);
  });

  return (
    <div className="post">
      <div className="post__header">
        <Avatar
          className="post__header__avatar"
          alt="usernameBoi"
          src={avatarUrl}
        />
        <h3 className="post__header__username">{username}</h3>
        <h4 className="post__header__expiration">
          Expires:
          {formattedTimeLeft}
        </h4>
      </div>
      <img
        className="post__image"
        src={imgUrl}
        alt=""
      />
      { isRefrying
        ? <Rings className="post__refry" color="#00BFFF" height={50} width={50} />
        : <input className="post__refry" type="button" value="refry" onClick={handleRefry} />}
      <h4 className="post__text">
        <strong>
          {username}
          {' '}
        </strong>
        {caption}
      </h4>
    </div>
  );
}

export default Post;
