const authService = require('../services/authService');

const loginUser = async (req, res) => {
    const { email, password } = req.body;

    try {
        const result = await authService.loginUser(email, password);
        if (result.error) {
            return res.status(400).json({ msg: result.error });
        }
        res.json({ token: result.token });
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server error');
    }
};

module.exports = {
    loginUser
};
