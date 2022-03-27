import './Post.css';
import React from 'react';
import Avatar from '@material-ui/core/Avatar';

function Post({username='username', avatarUrl='https://i.redd.it/b67mzvcj3fl81.jpg', caption='lorem ipsum', imgUrl='https://i.redd.it/j6a5ve7jtxl81.jpg', expiration=420}) {
  return (
    <div className='post'>
      <div className='post__header'>
        <Avatar
         className='post__header__avatar'
         alt='usernameBoi'
         src={avatarUrl}
        />
        <h3 className='post__header__username'>{username}</h3>
        <h4 className='post__header__expiration'>Expires: {expiration}</h4>
      </div>
      <img
        className='post__image'
        src={imgUrl}
        alt=''
      />
      {/* header -> avatar -> username */}
      <h4 className='post__text'><strong>{username} </strong>{caption}</h4>
    </div>
  )
}

export default Post
