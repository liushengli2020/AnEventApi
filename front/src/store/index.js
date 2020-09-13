import Vue from 'vue';
import Vuex from 'vuex';

import { account } from './account-module';
import { alert } from './alert-module';
import { event } from './event-module';
import { signup } from './signup-module';

Vue.use(Vuex);

export const store = new Vuex.Store({
  modules: {
    alert,
    account,
    event,
    signup,
  }
});
