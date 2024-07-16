const axios = require('axios');

// Example function to call Flask API to extract features
const extractFeaturesFromText = async (text) => {
    try {
        const response = await axios.post('http://localhost:5000/api/extract-features', { text });
        return response.data; // Extracted features
    } catch (error) {
        console.error('Error calling Python API:', error.message);
        throw new Error('API request failed');
    }
};

module.exports = {
    extractFeaturesFromText
};