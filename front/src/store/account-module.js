import { userService } from '../services';
import { router } from '../routers';

const user = JSON.parse(localStorage.getItem('user'));
const state = {status: { loggedIn: false, isAdmin: false }, user}

if(user && user.adminKey){
    state.status= { loggedIn: true, isAdmin: true };
    state.user = user;
}
else if(user){
    state.status = { loggedIn: true };
    state.user = user;
}
const actions = {
    async login({ dispatch, commit }, { email, password }) {
        commit('loginRequest', { email });
        try{
            const user = await userService.login(email, password);
            commit('loginSuccess', user);
            router.push('/');
        }
        catch(error){
            commit('loginFailure', error);
            dispatch('alert/error', error, { root: true });
        }
    },
    logout({ commit }) {
        userService.logout();
        commit('logout');
    },
    async register({ dispatch, commit }, user) {
        commit('registerRequest', user);
        try{
            const resp = await userService.register(user);
            commit('registerSuccess', resp);
            router.push('/signin');
            setTimeout(() => {
                // display success message after route change completes
                dispatch('alert/success', 'Registration successful', { root: true });
            })
        }
        catch(error){
            commit('registerFailure', error);
            dispatch('alert/error', error, { root: true });
        }
    }
};

const mutations = {
    loginRequest(state, user) {
        state.status = { loggingIn: true };
        state.user = user;
    },
    loginSuccess(state, user) {

        state.status = { loggedIn: true };
        if(user && user.adminKey){
            state.status = { loggedIn: true, isAdmin: true };
        }
        else{
            state.status = { loggedIn: true, isAdmin: false };
        }
        state.user = user;
    },
    loginFailure(state) {
        state.status = { loggedIn: false, isAdmin: false };
        state.user = null;
    },
    logout(state) {
        state.status = { loggedIn: false, isAdmin: false };
        state.user = null;
    },
    registerRequest(state, user) {
        state.status = { registering: true };
    },
    registerSuccess(state, user) {
        state.status = { loggedIn: false, isAdmin: false };
    },
    registerFailure(state, error) {
        state.status = { loggedIn: false, isAdmin: false };
    }
};

export const account = {
    namespaced: true,
    state,
    actions,
    mutations
};
