const mongoose = require('mongoose');

const candidateSchema = new mongoose.Schema({
    name: { type: String, required: true },
    jobTitle: { type: String },
    experienceYears: { type: Number },
    educationLevel: { type: String },
    certifications: [{ type: String }],
    location: { type: String }
});

module.exports = mongoose.model('Candidate', candidateSchema);
