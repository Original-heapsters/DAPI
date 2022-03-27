import './Header.css';
import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import FileUploadPage from './FileUpload';

function Header({overlayClick, avatarUrl, username}) {
  return (
    <div className="header">
      <img
        className="header__image"
        src="https://www.instagram.com/static/images/web/mobile_nav_type_logo.png/735145cfe0a4.png"
        alt=""
      />
      <div className='header__admin'>
        <input type='image' className='header__admin__upload' src={process.env.PUBLIC_URL + '/upload.png'} onClick={overlayClick} alt='Create fry'/>
        <Avatar
         className='header__admin__avatar'
         alt='usernameBoi'
         src={avatarUrl}
        />
        <h3 className='header__admin__username'>{username}</h3>
      </div>
    </div>
  )
}

export default Header
