const express = require('express');
const connectDB = require('./config/db');
require('dotenv').config();

// Connect to MongoDB
connectDB();

// Initialize Express
const app = express();

app.use(bodyParser.json());

// Middleware
app.use(express.json({ extended: false }));

// Define Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/users', require('./routes/users'));
app.use('/api/candidates', require('./routes/candidates')); // Include candidates routes
app.use('/api/generate', require('./routes/generate-ai')); // Generate the AI endpoint

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));

module.exports = app;
