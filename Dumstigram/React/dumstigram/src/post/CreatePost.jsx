import '../styles/CreatePost.css';
import { Rings } from 'react-loader-spinner';
import React, { useState, useEffect } from 'react';
import * as api from '../api';

function CreatePost({
  username,
  avatarUrl,
  setPostData,
}) {
  const [caption, setCaption] = useState('Toasty');
  const [ttl, setTtl] = useState('43200');
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');
  const [selectedFile, setSelectedFile] = useState();
  const [filters, setFilters] = useState();
  const [isLoadingFilters, setIsLoadingFilters] = useState(true);

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
    const postData = {
      url: uploadUrl,
      postBody: formData,
    };
    setPostData(postData);
  };

  // const handleSubmission = () => {
  //   const uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/posts`;
  //   const formData = new FormData();
  //   if (document.querySelector('input[type="checkbox"]:checked')) {
  //     const isoFilters = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'));
  // const filterList = isoFilters.reduce((str, filter) => `${filter.value},${str}`, '.slice(0, -1);
  //     formData.append('filters', filterList);
  //   }
  //
  //   formData.append('file', selectedFile);
  //   formData.append('username', username);
  //   formData.append('caption', caption);
  //   formData.append('ttl', ttl);
  //   formData.append('avatar', avatarUrl);
  //   const postData = {
  //     url: uploadUrl,
  //     postBody: formData,
  //   };
  //   setPostData(postData);
  // };

  return (
    <div className="createPost">
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
        </div>
      </div>
    </div>
  );
}

export default CreatePost;
