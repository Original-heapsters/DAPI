import '../styles/Header.css';
import React from 'react';
import Avatar from '@material-ui/core/Avatar';

function Header({
  overlayClick, avatarUrl, username, triggerLogin,
}) {
  const handleLogin = () => {
    triggerLogin('testing', 'https://i.pinimg.com/236x/b7/91/52/b79152a9f75782757086d5d13489f6d1--ugly-guys-guy-pictures.jpg');
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
        <h3 className="header__admin__username" onClick={handleLogin}>{username}</h3>
      </div>
    </div>
  );
}

export default Header;
