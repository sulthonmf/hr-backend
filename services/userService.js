const bcrypt = require('bcryptjs');
const User = require('../models/User');
const mongoose = require('mongoose');

const registerUser = async ({ username, email, password, role = 'user' }) => {
    try {
        // Check if the user already exists
        let user = await User.findOne({ email });

        if (user) {
            throw new Error('User already exists');
        }

        // Create a new user instance
        const newUser = new User({
            username,
            email,
            password,
            role
        });

        // Hash the password before saving it to the database
        const salt = await bcrypt.genSalt(10);
        newUser.password = await bcrypt.hash(password, salt);

        // Save the user to the database
        await newUser.save();
        mongoose.connection.close();

        return newUser; // Return the newly created user object
    } catch (err) {
        console.error(err.message);
        throw new Error('Server error'); // Handle server errors gracefully
    }
};

const getUserById = async (userId) => {
    try {
        // Fetch the user by their unique ID
        const user = await User.findById(userId).select('-password');

        return user; // Return the user object excluding the password field
    } catch (err) {
        console.error(err.message);
        throw new Error('Server error'); // Handle server errors gracefully
    }
};

module.exports = {
    registerUser,
    getUserById
};