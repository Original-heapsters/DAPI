import axios from 'axios';

async function fakeLogin(postInfo) {
  const { data } = await axios({
    url: `${process.env.REACT_APP_BACKEND_SERVER}/users/login/fake`,
    data: postInfo,
    method: 'POST',
  });
  return data.avatar_url;
}

export default fakeLogin;
