import axios from 'axios';
import React, { useState } from 'react';

function FileUploadPage(){
  const [selectedFile, setSelectedFile] = useState();
	const [isFilePicked, setIsFilePicked] = useState(false);

  const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
		setIsFilePicked(true);
	};

  const handleSubmission = () => {
    const formData = new FormData();

    formData.append('file', selectedFile);

    axios({
        url: `${process.env.REACT_APP_BACKEND_SERVER}/home`,
        params: { asApi: true },
        data: formData,
        method: 'POST',
        headers: { "Content-Type": "multipart/form-data" },
    })
      .then((response) => window.location.reload(false))
      .catch((error) => {
        console.error('Error:', error);
      });
  };

	return(
   <div>
			<input type="file" name="file" onChange={changeHandler} />
			<div>
				<button onClick={handleSubmission}>Submit</button>
			</div>
		</div>
	)
}

export default FileUploadPage;
