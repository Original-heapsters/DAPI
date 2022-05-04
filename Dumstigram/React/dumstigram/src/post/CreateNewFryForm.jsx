import '../styles/CreateNewFryForm.css';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from 'react-bootstrap/Modal';
import Stack from 'react-bootstrap/Stack';
import NewFryDetails from './NewFryDetails';

function CreateNewFryForm({
  setSelectedFile,
  setCaption,
  setExpiration,
}) {
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');

  const changeHandler = (event) => {
    const tmppath = URL.createObjectURL(event.target.files[0]);
    setSelectedFileUrl(tmppath);
    setSelectedFile(event.target.files[0]);
  };

  return (
    <Modal.Body>
      <Stack gap={3}>
        <div className="createPost__preview">
          <img
            className="createPost__image"
            src={selectedFileUrl}
            alt=""
          />
          <input type="file" name="file" onChange={changeHandler} />
        </div>
        <NewFryDetails
          setCaption={setCaption}
          setExpiration={setExpiration}
        />
      </Stack>
    </Modal.Body>
  );
}

export default CreateNewFryForm;
