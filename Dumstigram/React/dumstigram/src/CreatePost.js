import './CreatePost.css';
import React, {useState, useEffect} from 'react';
import axios from 'axios';
import Avatar from '@material-ui/core/Avatar';
import FileUpload from './FileUpload.js';

function CreatePost({overlayClick}) {
  const [username, setUsername] = useState('dumsty');
  const [caption, setCaption] = useState('Toasty');
  const [avatarUrl, setAvatarUrl] = useState('https://i.redd.it/b67mzvcj3fl81.jpg');
  const [ttl, setTtl] = useState('43200');
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');
  const [selectedFile, setSelectedFile] = useState();
  const [filters, setFilters] = useState();
	const [isFilePicked, setIsFilePicked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingFilters, setIsLoadingFilters] = useState(true);

  useEffect(() => {
    setIsLoadingFilters(true);
    axios({
        url: `${process.env.REACT_APP_BACKEND_SERVER}/filters`,
        method: 'GET',
        headers: {}
    }).then((response) => {
      const filters = response.data.map((filter) => {
        return {
          id: filter
        };
      });
      setFilters(filters);
      setIsLoadingFilters(false);
    })
    .catch((error) => {
      setIsLoadingFilters(false);
      console.log(error);
    });
  }, []);

  const changeHandler = (event) => {
		setIsFilePicked(true);
    const tmppath = URL.createObjectURL(event.target.files[0]);
    setSelectedFileUrl(tmppath);
    setSelectedFile(event.target.files[0]);
	};

  const handleSubmission = () => {
    setIsLoading(true);
    let uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/posts`;
    if (document.querySelector('input[name="selected_filter"]:checked')){
      const isoFilter = document.querySelector('input[name="selected_filter"]:checked').value
      uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/filters/${isoFilter}`;
    }
    const formData = new FormData();

    formData.append('file', selectedFile);
    // formData.append("document", JSON.stringify(documentJson));
    formData.append('username', username);
    formData.append('caption', caption);
    formData.append('ttl', ttl);
    formData.append('avatar', avatarUrl);

    axios({
        url: uploadUrl,
        data: formData,
        method: 'POST',
    })
      .then((response) => {
        setIsLoading(false);
        window.location.reload(false);
        overlayClick();
      })
      .catch((error) => {
        setIsLoading(false);
        console.error('Error:', error);
        overlayClick();
      });
  };

  return (
    <div className='createPost'>
      <div className='createPost__header'>
        <h2>Create new Fry</h2>
      </div>
      <div className='createPost__body'>
        <div className='createPost__preview'>
          <img
            className='createPost__image'
            src={selectedFileUrl}
            alt=''
          />
        </div>
        <div className='createPost__form'>
          { isLoadingFilters
            ?<div/>
            :
            filters.map((filter) => {
              return (<div key={filter.id} className='createPost__form__radio'>
                <input type="radio" id={filter.id} name='selected_filter' value={filter.id}/>
                <label id={filter.id}>{filter.id}</label>
              </div>);
            })
          }
          <label>Username:
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>
          <br/>
          <label>Caption:
            <input
              type="text"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
            />
          </label>
          <br/>
          <label>Avatar url:
            <input
              type="text"
              value={avatarUrl}
              onChange={(e) => setAvatarUrl(e.target.value)}
            />
          </label>
          <br/>
          <label>post ttl:
            <input
              type="text"
              value={ttl}
              onChange={(e) => setTtl(e.target.value)}
            />
          </label>
          <br/>
          <input type="file" name="file" onChange={changeHandler} />
          <div>
              <button onClick={handleSubmission}>Submit</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CreatePost
