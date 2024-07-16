const candidateService = require('../services/candidateService');

// Controller function to handle creating a new candidate
const createCandidate = async (req, res) => {
    const {
        name,
        jobTitle,
        experienceYears,
        educationLevel,
        certifications,
        location
    } = req.body;

    try {
        const newCandidate = await candidateService.createCandidate({
            name,
            jobTitle,
            experienceYears,
            educationLevel,
            certifications,
            location
        });

        res.json(newCandidate);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server error');
    }
};

// Controller function to handle retrieving candidates by job position
const getCandidatesByPosition = async (req, res) => {
    const position = req.params.position;

    try {
        const candidates = await candidateService.getCandidatesByPosition(position);
        res.json(candidates);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server error');
    }
};

module.exports = {
    createCandidate,
    getCandidatesByPosition
};
