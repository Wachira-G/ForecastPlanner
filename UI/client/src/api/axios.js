import axios ffrom 'axios';

const BASE_URL = 'https://forecast-planner-b6f6e7dba956.herokuapp.com';

export default axios.create({
  baseURL: BASE_URL;
});

export const axiosPrivate = axios.create(
  baseURL: BASE_URL,
  headers: {'Content-Type': 'application/json'},
  withCredentials: true;
)
