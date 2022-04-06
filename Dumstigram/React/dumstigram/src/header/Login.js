import '../styles/Login.css';
import React, {useState, useEffect} from 'react';

function Login({overlayClick, username, avatarUrl}) {
  const [caption, setCaption] = useState('Toasty');
  const [ttl, setTtl] = useState('43200');
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');
  const [selectedFile, setSelectedFile] = useState();
  const [filters, setFilters] = useState();
  const [isLoadingFilters, setIsLoadingFilters] = useState(true);

  useEffect(() => {
  }, []);

  const changeHandler = (event) => {
    const tmppath = URL.createObjectURL(event.target.files[0]);
    setSelectedFileUrl(tmppath);
    setSelectedFile(event.target.files[0]);
	};

  const handleSubmission = () => {
    let uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/posts`;
    if (document.querySelector('input[name="selected_filter"]:checked')){
      const isoFilter = document.querySelector('input[name="selected_filter"]:checked').value
      uploadUrl = `${process.env.REACT_APP_BACKEND_SERVER}/posts/${isoFilter}`;
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
        window.location.reload(false);
        overlayClick();
      })
      .catch((error) => {
        console.error('Error:', error);
        overlayClick();
      });
  };

  return (
    <div className='createPost'>
      <div className='createPost__header'>
        <h2>Create new Fry</h2>
        <input
          className='createPost__header__closeButton'
          type="button"
          value='X'
          onClick={overlayClick}
        />
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
          <br/>
          <label>Caption:
            <input
              type="text"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
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

export default Login
