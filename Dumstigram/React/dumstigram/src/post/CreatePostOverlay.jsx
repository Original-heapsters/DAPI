import '../styles/CreatePostOverlay.css';
import React from 'react';
import CreatePost from './CreatePost';

function CreatePostOverlay({
  creatingPost, overlayClick, username, avatarUrl, triggerRefresh,
}) {
  return (
    <div className="createPostOverlay">
      { !creatingPost
        ? (
          <div className="createPostOverlay__overlay">
            <CreatePost
              overlayClick={overlayClick}
              username={username}
              avatarUrl={avatarUrl}
              triggerRefresh={triggerRefresh}
            />
          </div>
        )
        : <div />}

    </div>
  );
}

export default CreatePostOverlay;
