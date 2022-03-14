import './Header.css';
import React from 'react';
import FileUploadPage from './FileUpload';

function Header() {
  return (
    <div className="header">
      <img
        className="header__image"
        src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png"
        alt=""
      />
      <FileUploadPage/>
    </div>
  )
}

export default Header
