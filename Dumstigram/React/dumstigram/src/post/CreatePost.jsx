import '../styles/CreatePost.css';
import { Rings } from 'react-loader-spinner';
import React, { useState, useEffect } from 'react';
import * as api from '../api';

function CreatePost({
  overlayClick,
  username,
  avatarUrl,
  triggerRefresh,
}) {
  const [caption, setCaption] = useState('Toasty');
  const [ttl, setTtl] = useState('43200');
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');
  const [selectedFile, setSelectedFile] = useState();
  const [filters, setFilters] = useState();
  const [isLoadingFilters, setIsLoadingFilters] = useState(true);
  const [isPosting, setIsPosting] = useState(false);

  useEffect(() => {
    setIsLoadingFilters(true);
    async function getFilters() {
      const possibleFilters = await api.getFilters();
      return possibleFilters;
    }
    getFilters()
      .then((possFilters) => {
        setFilters(possFilters);
        setIsLoadingFilters(false);
      })
      .catch(() => {
        setIsLoadingFilters(false);
      });
  }, []);

  const changeHandler = (event) => {
    const tmppath = URL.createObjectURL(event.target.files[0]);
    setSelectedFileUrl(tmppath);
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmission = () => {
    setIsPosting(true);
    const uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/posts`;
    const formData = new FormData();
    if (document.querySelector('input[type="checkbox"]:checked')) {
      const isoFilters = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'));
      const filterList = isoFilters.reduce((str, filter) => `${filter.value},${str}`, '').slice(0, -1);
      formData.append('filters', filterList);
    }

    formData.append('file', selectedFile);
    formData.append('username', username);
    formData.append('caption', caption);
    formData.append('ttl', ttl);
    formData.append('avatar', avatarUrl);

    async function createPost(url, postBody) {
      await api.createPost(url, postBody);
    }
    createPost(uploadUrl, formData)
      .then(() => {
        setIsPosting(false);
        triggerRefresh();
        overlayClick();
      })
      .catch(() => {
        setIsPosting(false);
        overlayClick();
      });
  };

  return (
    <div className="createPost">
      <div className="createPost__header">
        <h2>Create new Fry</h2>
        <input
          className="createPost__header__closeButton"
          type="button"
          value="X"
          onClick={overlayClick}
        />
      </div>
      <div className="createPost__body">
        <div className="createPost__preview">
          <img
            className="createPost__image"
            src={selectedFileUrl}
            alt=""
          />
        </div>
        <div className="createPost__form">
          { isLoadingFilters
            ? <Rings color="#00BFFF" height={50} width={50} />
            : filters.map((filter) => (
              <div key={filter.id} className="createPost__form__radio">
                <input type="checkbox" id={filter.id} name="selected_filter" value={filter.id} />
                <label htmlFor={filter.id} id={filter.id}>{filter.id}</label>
              </div>
            ))}
          <br />
          <label htmlFor="caption">
            Caption:
            <input
              id="caption"
              type="text"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
            />
          </label>
          <br />
          <label htmlFor="ttl">
            post ttl:
            <input
              id="ttl"
              type="text"
              value={ttl}
              onChange={(e) => setTtl(e.target.value)}
            />
          </label>
          <br />
          <input type="file" name="file" onChange={changeHandler} />
          <div>
            { isPosting
              ? <Rings color="#00BFFF" height={50} width={50} />
              : <button type="button" onClick={handleSubmission}>Submit</button>}

          </div>
        </div>
      </div>
    </div>
  );
}

export default CreatePost;
