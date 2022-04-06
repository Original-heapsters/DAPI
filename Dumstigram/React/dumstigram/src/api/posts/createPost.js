import axios from 'axios';

async function createPost(url, data) {
  await axios({
    url,
    data,
    method: 'POST',
  });
}

export default createPost;
