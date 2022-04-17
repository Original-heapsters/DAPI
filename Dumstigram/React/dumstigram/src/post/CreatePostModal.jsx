import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from 'react-bootstrap/Modal';
import { Rings } from 'react-loader-spinner';
import Button from 'react-bootstrap/Button';
import CreatePost from './CreatePost';
import * as api from '../api';

function CreateModalForm({
  creatingPost, closeModal, username, avatarUrl, triggerRefresh,
}) {
  const [isPosting, setIsPosting] = useState(false);
  const [postData, setPostData] = useState();

  const handleSubmission = () => {
    console.log(JSON.stringify(postData));
    setIsPosting(true);
    const { url: uploadUrl, postBody: formData } = postData;
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
    <Modal show={!creatingPost} onHide={closeModal} fullscreen>
      <Modal.Header closeButton>
        <Modal.Title>Create New Fry</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <CreatePost
          overlayClick={closeModal}
          username={username}
          avatarUrl={avatarUrl}
          triggerRefresh={triggerRefresh}
          setPostData={setPostData}
        />
      </Modal.Body>
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

export default CreateModalForm;
