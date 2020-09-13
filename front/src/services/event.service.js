import { config } from '../config';
const axios = require('axios')

export const eventService = {
    getAllEvents,
};

async function getAllEvents() {
    try{
        const resp = await axios.get(`${config.apiUrl}/events` );
        let events;
        if (resp.data.status === 'success') {
            events = resp.data.data;
        }
        return events;
    }
    catch (e) {
        throw e;
    }
}

