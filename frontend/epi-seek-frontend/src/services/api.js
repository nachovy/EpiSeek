import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export const fetchAnswer = async (question, top_k) => {
    const response = await axios.get(`${API_BASE}/ask`, {
        params: {
            question: encodeURIComponent(question),
            top_k: top_k
        }
    });
    return response.data;
};

export const fetchFollowUpAnswer = async (question) => {
    const response = await axios.get(`${API_BASE}/ask`, {
        params: {
            question: encodeURIComponent(question),
            follow_up: true
        }
    });
    return response.data;
};
