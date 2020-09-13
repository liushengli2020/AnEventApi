<template>
    <div class="jumbotron offset-sm-1" v-if="alert.message">
        <div :class="`alert ${alert.type}`">{{alert.message}}</div>
    </div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'

    export default {
        name: 'app',
        computed: {
            ...mapState({
                alert: state => state.alert
            })
        },
        methods: {
            ...mapActions({
                clearAlert: 'alert/clear'
            })
        },
        watch: {
            $route (){
                // clear alert on location change
                this.clearAlert();
            }
        }
    };
</script>
