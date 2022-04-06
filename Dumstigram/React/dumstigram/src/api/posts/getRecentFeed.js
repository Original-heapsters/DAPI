import axios from 'axios';

const getRecent = async (numItems) => {
  const { data } = await axios({
    url: `${process.env.REACT_APP_BACKEND_SERVER}/recent/${numItems}`,
    method: 'GET',
    headers: {},
  });

  const recentPosts = Object.keys(data).map((recent) => {
    const post = data[recent];
    return {
      id: recent,
      post: {
        ...post,
        img_url: `${process.env.REACT_APP_BACKEND_SERVER}${post.img_url.substr(1)}`,
      },
    };
  });

  return recentPosts;
};

export default getRecent;
