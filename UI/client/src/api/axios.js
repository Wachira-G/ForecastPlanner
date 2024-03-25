import axios from 'axios';

const BASE_URL = 'https://forecast-planner-b6f6e7dba956.herokuapp.com/api/v1/';

export default axios.create({
    baseURL: BASE_URL
});

export const axiosPrivate = axios.create({
    baseURL: BASE_URL,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
});
