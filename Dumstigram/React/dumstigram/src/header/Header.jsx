import '../styles/Header.css';
import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import LoginModal from './LoginModal';
import * as api from '../api';

function Header({
  triggerLogin, overlayClick, avatarUrl, username, setUsername,
}) {
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [selectedFile, setSelectedFile] = useState();
  const handleLogin = () => {
    setIsLoggingIn(true);
  };

  const handleLoginAbort = () => {
    setIsLoggingIn(false);
  };

  const loginSubmit = () => {
    async function fakeLogin(postInfo) {
      const url = await api.fakeLogin(postInfo);
      return url;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('username', username);

    fakeLogin(formData)
      .then((avatarSuffix) => {
        const fullAvatar = `${process.env.REACT_APP_BACKEND_SERVER}${avatarSuffix.substr(1)}`;
        triggerLogin(username, fullAvatar);
        setIsLoggingIn(false);
      });
  };

  return (
    <div className="header">
      <img
        className="header__image"
        src={`${process.env.PUBLIC_URL}/logo.png`}
        alt=""
      />
      <div className="header__admin">
        <input type="image" className="header__admin__upload" src={`${process.env.PUBLIC_URL}/upload.png`} onClick={overlayClick} alt="Create fry" />
        <Avatar
          className="header__admin__avatar"
          alt="usernameBoi"
          src={avatarUrl}
          onClick={handleLogin}
        />
        <LoginModal
          loggingIn={isLoggingIn}
          closeModal={handleLoginAbort}
          avatarUrl={avatarUrl}
          username={username}
          login={loginSubmit}
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          setUsername={setUsername}
        />
        <h3 className="header__admin__username">{username}</h3>
      </div>
    </div>
  );
}

export default Header;
