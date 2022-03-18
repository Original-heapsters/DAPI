import './CreatePostOverlay.css'
import React, { useState } from 'react';
import CreatePost from './CreatePost.js';

function CreatePostOverlay({creatingPost, overlayClick}){

	return(
		<div className='createPostOverlay'>
			{ !creatingPost
			? <div className='createPostOverlay__overlay'>
					<CreatePost overlayClick={overlayClick}/>
			</div>
			:<div/>
		}

		</div>
	)
}

export default CreatePostOverlay;
