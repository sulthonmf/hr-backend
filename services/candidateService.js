const Candidate = require('../models/Candidate');
const mongoose = require('mongoose');

const createCandidate = async ({
    name,
    jobTitle,
    experienceYears,
    educationLevel,
    certifications,
    location
}) => {
    try {
        // Create a new candidate instance
        const newCandidate = new Candidate({
            name,
            jobTitle,
            experienceYears,
            educationLevel,
            certifications,
            location
        });

        // Save the candidate to the database
        const candidate = await newCandidate.save();
        mongoose.connection.close();

        return candidate; // Return the newly created candidate object
    } catch (err) {
        console.error(err.message);
        throw new Error('Server error'); // Handle server errors gracefully
    }
};

const getCandidatesByPosition = async (position) => {
    try {
        // Fetch candidates based on job position
        const candidates = await Candidate.find({ jobTitle: position });

        return candidates; // Return array of candidates matching the position
    } catch (err) {
        console.error(err.message);
        throw new Error('Server error'); // Handle server errors gracefully
    }
};

module.exports = {
    createCandidate,
    getCandidatesByPosition
};