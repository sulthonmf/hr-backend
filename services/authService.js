const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const User = require('../models/User');
require('dotenv').config();

const generateToken = (user) => {
    const payload = {
        user: {
            id: user.id,
            role: user.role
        }
    };

    return jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '1h' });
};

const loginUser = async (email, password) => {
    try {
        let user = await User.findOne({ email });

        if (!user) {
            return { error: 'User not found' };
        }

        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            return { error: 'Invalid credentials' };
        }

        const token = generateToken(user);
        return { token };
    } catch (err) {
        console.error(err.message);
        throw new Error('Server error');
    }
};

module.exports = {
    loginUser
};
