const express = require('express');
const router = express.Router();
const candidateController = require('../controllers/candidateController');

// Route to create a new candidate
router.post('/create', candidateController.createCandidate);

// Route to get candidates by job position
router.get('/:position', candidateController.getCandidatesByPosition);

module.exports = router;
