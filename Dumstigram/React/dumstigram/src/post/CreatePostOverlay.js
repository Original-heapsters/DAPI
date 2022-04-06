import '../styles/CreatePostOverlay.css'
import React from 'react';
import CreatePost from './CreatePost.js';

function CreatePostOverlay({creatingPost, overlayClick, username, avatarUrl}){

	return(
		<div className='createPostOverlay'>
			{ !creatingPost
			? <div className='createPostOverlay__overlay'>
					<CreatePost overlayClick={overlayClick} username={username} avatarUrl={avatarUrl}/>
			</div>
			:<div/>
		}

		</div>
	)
}

export default CreatePostOverlay;
