import { config } from '../config';
import crypto from 'crypto'
const axios = require('axios')

export const signupService = {
    getAllSignups,
    signupEvent,
    quitEvent,
};

async function getAllSignups(eventId, adminId, adminKey) {
    try{
        const path = `/event/${eventId}/users`;
        const url = new URL(`${config.apiUrl}${path}`);
        const signature = crypto.createHmac('sha256', adminKey).update(url.pathname).digest('hex');
        const resp = await axios.get(url.href,
            { headers: { admin_signature: signature, admin_id:adminId }} );
        let signups;
        if (resp.data.status === 'success') {
            signups = resp.data.data;
        }
        return signups;
    }
    catch (e) {
        throw e;
    }
}

async function signupEvent(key, eventId, userId, adminId, adminKey) {
    try {
        if( typeof userId === 'string'){
            userId = parseInt(userId);
        }
        if( typeof adminId === 'string'){
            adminId = parseInt(adminId);
        }
        const path = `/event/${eventId}/users`;
        const url = new URL(`${config.apiUrl}${path}`);
        let signature;
        let adminSignature;
        if (adminKey) {
            adminSignature = crypto.createHmac('sha256', adminKey).update(url.pathname).digest('hex');
        } else {
            signature = crypto.createHmac('sha256', key).update(url.pathname).digest('hex')
        }
        let resp;
        const json = JSON.stringify({user_id: userId});
        if (adminSignature) {
            resp = await axios.post(url.href,
                json,
                {headers: {admin_signature: adminSignature, admin_id: adminId, 'Content-Type': 'application/json'}});
        } else {
            resp = await axios.post(url.href,
                json,
                {headers: {signature: signature, 'Content-Type': 'application/json'}});
        }
        if(resp && resp.data.status === 'success'){
            return true;
        }
        return false;
    }
    catch (e) {
        throw e;
    }
}


async function quitEvent(key, eventId, userId, adminId, adminKey) {
    try {
        if( typeof userId === 'string'){
            userId = parseInt(userId);
        }
        if( typeof adminId === 'string'){
            adminId = parseInt(adminId);
        }
        const path = `/event/${eventId}/user/${userId}`;
        const url = new URL(`${config.apiUrl}${path}`);
        let signature;
        let adminSignature;
        if (adminKey) {
            adminSignature = crypto.createHmac('sha256', adminKey).update(url.pathname).digest('hex');
        } else {
            signature = crypto.createHmac('sha256', key).update(url.pathname).digest('hex')
        }
        let resp;
        if (adminSignature) {
            resp = await axios.delete(url.href,
                {headers: {admin_signature: adminSignature, admin_id: adminId}});
        } else {
            resp = await axios.delete(url.href,
                {headers: {signature: signature}});
        }
        if(resp && resp.data.status === 'success'){
            return true;
        }
        return false;
    }
    catch (e) {
        throw e;
    }
}
