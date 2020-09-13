<template>
    <div class="account" >
        <button class="btn btn-primary" @click="$router.push('signup')" v-if="!signedIn && !isInSigninOrSignup">
            Register
        </button>
        <button class="btn btn-primary" style="margin-left: 2rem" @click="$router.push('signin')" v-if="!signedIn && !isInSigninOrSignup">
            Login
        </button>
        <button class="btn btn-primary" @click="signout()" v-if="signedIn">
            Logout
        </button>
    </div>
</template>

<script>
    import { mapActions } from 'vuex'

    export default {
        data () {
            return {
                isInSigninOrSignup: this.$router.currentRoute.path=='/signin'
                    || this.$router.currentRoute.path=='/signup',
            }
        },
        computed: {
            signedIn () {
                return this.$store.state.account.status.loggedIn;
            }
            // ...mapState({
            //     account: state => state.account,
            // })
        },
        created () {
        },
        methods: {
            ...mapActions('account', ['logout']),
            signout () {
                this.logout();
                this.$router.push('signin');
            }
        },
        watch:{
            $route (to, from){
                if(to.path ==='/signup' || to.path ==='/signin')
                    this.$data.isInSigninOrSignup=true
                else
                    this.$data.isInSigninOrSignup=false
            }
        }
    };
</script>
