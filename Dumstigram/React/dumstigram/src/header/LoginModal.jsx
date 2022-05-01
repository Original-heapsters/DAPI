import '../styles/LoginModal.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import LoginForm from './LoginForm';

function CreateModalForm({
  loggingIn, closeModal, login, setUsername, setSelectedFile, selectedFile,
}) {
  return (
    <Modal show={loggingIn} onHide={closeModal} dialogClassName="modal-90w">
      <Modal.Header closeButton>
        <Modal.Title>Login</Modal.Title>
      </Modal.Header>
      <LoginForm
        setSelectedFile={setSelectedFile}
        selectedFile={selectedFile}
        setUsername={setUsername}
      />
      <Modal.Footer>
        <Button variant="primary" onClick={login}>Submit</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default CreateModalForm;
