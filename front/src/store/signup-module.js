import {signupService} from '../services';
import {router} from "../routers";

const state = {
    all: {currentEventId: null}
};

const actions = {
    async getAllSignups({ dispatch, commit }, { eventId, user }) {
        commit('getAllRequest');
        try{
            const adminId = user.userId;
            const adminKey = user.adminKey;
            const signups = await signupService.getAllSignups(eventId, adminId, adminKey);
            commit('getAllSuccess', signups);
            router.push('/event-signup');
        }
        catch(error){
            commit('getAllFailure', error);
            dispatch('alert/error', error, { root: true });
        }
    },
    async quitEvent({ dispatch, commit }, { eventId, userId, user}) {
        commit('deleteRequest', userId);

        try{
            const success = await signupService.quitEvent( user.password, eventId, userId, user.userId, user.adminKey);
            if(success) {
                commit('deleteSuccess', userId);
                if(user.adminId)
                    router.push('/event-signup');
                else{
                    router.push('/');
                }
                dispatch('alert/success', `${userId} quit successful`, { root: true });
            }
            else{
                throw new Error('delete failed');
            }
        }
        catch(error){
            commit('deleteFailure', error);
            dispatch('alert/error', error, { root: true });
        }
    },
    async signupEvent({ dispatch, commit }, { eventId, userId, user}) {
        commit('addRequest', userId);

        try{
            const success = await signupService.signupEvent( user.password, eventId, userId, user.userId, user.adminKey);
            if(success) {
                commit('addSuccess', userId);
                if(user.adminId)
                    router.push('/event-signup');
                else{
                    router.push('/');
                }
                dispatch('alert/success', `${userId} signup successful`, { root: true });
            }
            else{
                throw new Error('delete failed');
            }
        }
        catch(error){
            commit('addFailure', error);
            dispatch('alert/error', error, { root: true });
        }
    }
};

const mutations = {
    getAllRequest(state) {
        state.all = { loading: true };
    },
    getAllSuccess(state, signups) {
        state.all = { items: signups };
    },
    getAllFailure(state, error) {
        state.all = { error };
    },
    deleteRequest(state, id) {
        // add 'deleting:true' property to user being deleted
        if(state.all.items)
            state.all.items = state.all.items.map(signup =>
                signup.id === id
                    ? { ...signup, deleting: true }
                    : signup
            );
    },
    deleteSuccess(state, id) {
        // remove deleted user from state
        if(state.all.items)
            state.all.items = state.all.items.filter(signup => signup.id !== id)
    },
    deleteFailure(state, { id, error }) {
        // remove 'deleting:true' property and add 'deleteError:[error]' property to user
        if(state.all.items)
            state.all.items = state.all.items.map(user => {
                if (user.id === id) {
                    // make copy of user without 'deleting:true' property
                    const { ...userCopy } = user;
                    // return copy of user with 'deleteError:[error]' property
                    return { ...userCopy, error };
                }
                return user;
            });
    },
    addRequest(state, id) {
        // add 'adding:true' property to user being added
        if(state.all.items)
            state.all.items = state.all.items.map(signup =>
                signup.id === id
                    ? { ...signup, adding: true }
                    : signup
            );
    },
    addSuccess(state, id) {
        // remove deleted user from state
        if(state.all.items)
            state.all.items = state.all.items.filter(signup => signup.id !== id)
    },
    addFailure(state, { id, error }) {
        // remove 'deleting:true' property and add 'deleteError:[error]' property to user
        if(state.all.items)
            state.all.items = state.all.items.map(user => {
                if (user.id === id) {
                    // make copy of user without 'deleting:true' property
                    const { ...userCopy } = user;
                    // return copy of user with 'deleteError:[error]' property
                    return { ...userCopy, error };
                }
                return user;
            });
    }
};

export const signup = {
    namespaced: true,
    state,
    actions,
    mutations
};
