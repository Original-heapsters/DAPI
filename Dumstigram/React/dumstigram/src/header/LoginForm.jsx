import '../styles/LoginForm.css';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from 'react-bootstrap/Modal';
import Stack from 'react-bootstrap/Stack';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

function LoginForm({
  setUsername, setAvatarUrl,
}) {
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');
  const [selectedFile, setSelectedFile] = useState();
  const changeHandler = (event) => {
    const tmppath = URL.createObjectURL(event.target.files[0]);
    console.log(tmppath);
    setAvatarUrl(tmppath);
    setSelectedFileUrl(tmppath);
    setSelectedFile(event.target.files[0]);
  };

  const handleUsernameChange = (event) => {
    const fieldVal = event.target.value;
    setUsername(fieldVal);
  };

  return (
    <Modal.Body>
      <Stack gap={2}>
        <div className="login__avatar__preview">
          <img
            className="login__avatar__image"
            src={selectedFileUrl}
            alt=""
          />
          <input type="file" name="file" onChange={changeHandler} />
        </div>
        <Stack direction="horizontal" gap={2}>
          <FloatingLabel className="me-auto" controlId="usernameInput" label="Username">
            <Form.Control type="email" placeholder="name@example.com" onChange={handleUsernameChange}/>
          </FloatingLabel>
        </Stack>
      </Stack>
    </Modal.Body>
  );
}

export default LoginForm;
