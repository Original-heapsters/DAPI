import axios from 'axios';

const getFilters = async () => {
  const { data } = await axios({
    url: `${process.env.REACT_APP_BACKEND_SERVER}/filters`,
    method: 'GET',
    headers: {},
  });
  const filters = data.map((filter) => ({
    id: filter.name,
    ...filter,
  }));
  return filters;
};

export default getFilters;
