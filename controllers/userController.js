const userService = require('../services/userService');

const registerUser = async (req, res) => {
    const { username, email, password, role } = req.body;

    try {
        const newUser = await userService.registerUser({
            username,
            email,
            password,
            role
        });

        res.json(newUser);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server error');
    }
};

module.exports = {
    registerUser
};
