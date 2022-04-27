import '../styles/Header.css';
import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import LoginModal from './LoginModal';

function Header({
  triggerLogin, overlayClick, avatarUrl, username, setUsername, setAvatarUrl,
}) {
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const handleLogin = () => {
    setIsLoggingIn(true);
  };

  const handleLoginAbort = () => {
    setIsLoggingIn(false);
  };

  const loginSubmit = () => {
    console.log(username)
    console.log(avatarUrl)
    triggerLogin(username, avatarUrl);
    setIsLoggingIn(false);
  }

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
          setUsername={setUsername}
          setAvatarUrl={setAvatarUrl}
        />
        <h3 className="header__admin__username">{username}</h3>
      </div>
    </div>
  );
}

export default Header;
