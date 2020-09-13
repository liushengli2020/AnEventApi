import { eventService } from '../services';

const state = {
    all: {}
};

const actions = {
    getAllEvents({ commit }) {
        commit('getAllRequest');
        eventService.getAllEvents()
            .then(
                events => commit('getAllSuccess', events),
                error => commit('getAllFailure', error)
            );
    },

};

const mutations = {
    getAllRequest(state) {
        state.all = { loading: true };
    },
    getAllSuccess(state, events) {
        state.all = { items: events };
    },
    getAllFailure(state, error) {
        state.all = { error };
    },
};

export const event = {
    namespaced: true,
    state,
    actions,
    mutations
};
