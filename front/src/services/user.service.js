import { config } from '../config';
import crypto from 'crypto'
const axios = require('axios')

export const userService = {
    login,
    logout,
    register,
};

async function login(email, password) {
    try{
        const sha256Hex = crypto.createHash('sha256').update(password).digest('hex');
        const resp = await axios.get(`${config.apiUrl}/user/email/${email}`, { headers: { password: sha256Hex }} );
        let user;
        if (resp.data.status === 'success') {
            user = {};
            user.userId = resp.data.data.user_id;
            user.adminKey = resp.data.data.admin_key;
            user.password = sha256Hex;
            localStorage.setItem('user',JSON.stringify(user));
        }
        return user;
    }
    catch (e) {
        logout();
        throw e;
    }
}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
}

async function register(user) {
    try{
        user.password = crypto.createHash('sha256').update(user.password).digest('hex');
        const json = JSON.stringify(user);
        const resp = await axios.post(`${config.apiUrl}/users`, json, { headers: { 'Content-Type': 'application/json' }} );
        if (resp.status === 'failure') {
            throw new Error(resp.data.message);
        }
    }
    catch (e) {
        throw e;
    }
}
