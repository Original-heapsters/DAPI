import './FileUpload.css'
import { Grid } from  'react-loader-spinner'
import axios from 'axios';
import React, { useState } from 'react';

function FileUploadPage({overlayClick}){
  const [selectedFile, setSelectedFile] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
	};

  const handleSubmission = () => {
    setIsLoading(true);
    const formData = new FormData();

    formData.append('file', selectedFile);

    axios({
        url: `${process.env.REACT_APP_BACKEND_SERVER}/home`,
        params: { asApi: true },
        data: formData,
        method: 'POST',
        headers: { "Content-Type": "multipart/form-data" },
    })
      .then((response) => {
        setIsLoading(false);
        window.location.reload(false);
      })
      .catch((error) => {
        setIsLoading(false);
        console.error('Error:', error);
      });
  };

	return(
   <div className='fileUpload'>
    { isLoading
      ? <div  className='fileUpload__spinner'><Grid color="#00BFFF" height={50} width={50} /></div>
      : <div>
          <input type='image' alt='upload' className='fileUpload__icon' src={process.env.PUBLIC_URL + '/upload.png'} onClick={overlayClick}/>
          <div className='fileUpload__form'>
            <input type="file" name="file" onChange={changeHandler} />
            <div>
                <button onClick={handleSubmission}>Submit</button>
            </div>
          </div>
        </div>
    }

		</div>
	)
}

export default FileUploadPage;
