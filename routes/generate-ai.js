const express = require('express');
const router = express.Router();
const { extractFeaturesFromText } = require('../controllers/generateAI');

// Run AI
router.post('/extract-features', async (req, res) => {
    try {
        const { text } = req.body;
        const features = await extractFeaturesFromText(text);
        res.json(features);
    } catch (error) {
        console.error('Error extracting features:', error.message);
        res.status(500).json({ error: 'Failed to extract features' });
    }
});

module.exports = router;