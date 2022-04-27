import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { Rings } from 'react-loader-spinner';
import CreateNewFryForm from './CreateNewFryForm';
import * as api from '../api';

function LoginModal({
  creatingPost, closeModal, username, avatarUrl, triggerRefresh,
}) {
  const [isPosting, setIsPosting] = useState(false);
  const [selectedFile, setSelectedFile] = useState();
  const [caption, setCaption] = useState('Toasty');
  const [expiration, setExpiration] = useState('43200');

  const handleSubmission = () => {
    setIsPosting(true);
    const uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/posts`;
    const formData = new FormData();
    console.log(username);
    formData.append('file', selectedFile);
    formData.append('username', username);
    formData.append('caption', caption);
    formData.append('ttl', expiration);
    formData.append('avatar', avatarUrl);

    if (document.querySelector('input[type="checkbox"]:checked')) {
      const isoFilters = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'));
      const filterList = isoFilters.reduce((str, filter) => `${filter.value},${str}`, '').slice(0, -1);
      formData.append('filters', filterList);
    }

    async function createPost(url, postBody) {
      await api.createPost(url, postBody);
    }
    createPost(uploadUrl, formData)
      .then(() => {
        setIsPosting(false);
        triggerRefresh();
        closeModal();
      })
      .catch(() => {
        setIsPosting(false);
        closeModal();
      });
  };

  return (
    <Modal show={!creatingPost} onHide={closeModal} dialogClassName="modal-90w">
      <Modal.Header closeButton>
        <Modal.Title>Create New Fry</Modal.Title>
      </Modal.Header>
      <CreateNewFryForm
        setSelectedFile={setSelectedFile}
        setCaption={setCaption}
        setExpiration={setExpiration}
      />
      <Modal.Footer>
        <div>
          { isPosting
            ? <Rings color="#00BFFF" height={50} width={50} />
            : <Button variant="primary" onClick={handleSubmission}>Submit</Button>}

        </div>
      </Modal.Footer>
    </Modal>
  );
}

export default LoginModal;
