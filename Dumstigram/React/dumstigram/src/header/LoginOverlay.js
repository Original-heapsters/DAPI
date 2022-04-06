import '../styles/LoginOverlay.css'
import React from 'react';
import Login from './Login.js';

function LoginOverlay({loggingIn, overlayClick, username, avatarUrl}){

	return(
		<div className='loginOverlay'>
			{ !loggingIn
			? <div className='loginOverlay__overlay'>
					<Login overlayClick={overlayClick} username={username} avatarUrl={avatarUrl}/>
			</div>
			:<div/>
		}

		</div>
	)
}

export default LoginOverlay;
