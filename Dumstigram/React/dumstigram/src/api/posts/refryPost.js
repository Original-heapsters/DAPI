import axios from 'axios';

async function refryPost(postKey, postInfo) {
  await axios({
    url: `${process.env.REACT_APP_BACKEND_SERVER}/posts/refry/${postKey}`,
    data: postInfo,
    method: 'POST',
  });
}

export default refryPost;
