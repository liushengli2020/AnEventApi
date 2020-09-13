/* eslint-disable no-console */
import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import { store } from './store'
import VeeValidate from 'vee-validate';
import { router } from './routers'

Vue.use(VeeValidate);

new Vue({
    vuetify,
    router,
    store,
    render: h => h(App)
}).$mount('#app')
