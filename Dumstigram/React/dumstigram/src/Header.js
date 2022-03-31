import './Header.css';
import React from 'react';
import Avatar from '@material-ui/core/Avatar';

function Header({overlayClick, avatarUrl, username}) {
  return (
    <div className="header">
      <img
        className="header__image"
        src={process.env.PUBLIC_URL + '/logo.png'}
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