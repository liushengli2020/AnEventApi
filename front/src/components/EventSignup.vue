<template>
    <div class="jumbotron">
        <div class="container">
            <div class="row">
                <div class="col-sm-0 offset-sm-0">
                    <table class="table table-striped">
                        <thead thead-light>
                        <tr>
                            <th scope="col" class="text-nowrap">id</th>
                            <th scope="col" class="text-nowrap">name</th>
                            <th scope="col" class="text-nowrap">email</th>
                            <th scope="col" class="text-nowrap" v-if="isAdmin">managerment</th>
                        </tr>
                        </thead>
                        <tbody v-if="signups.items">
                        <tr v-for="user in signups.items" :key="user.id">
                            <td class="text-nowrap">{{user.id}}</td>
                            <td class="text-nowrap">{{user.name}}</td>
                            <td class="text-nowrap">{{user.email}}</td>
                            <td class="text-nowrap" v-if="isAdmin">
                                <button class="btn btn-primary btn-sm ml-1" @click="alert('to do')" >
                                    remove
                                </button>
                            </td>
                        </tr>
                        <tr></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'

    export default {
        name: 'app',
        data () {
            return {
                userId: 0,
            }
        },
        computed: {
            ...mapState({
                signups: state => state.signup.all,
            }),
            isAdmin () {
                return this.$store.state.account.status.isAdmin;
            },
            user () {
                return this.$store.state.account.user;
            }
        },
        methods: {
            ...mapActions('event', ['getAllEvents']),
            ...mapActions('signup', ['getAllSignups', 'signupEvent','quitEvent']),
        },
        mounted () {
            this.getAllSignups({eventId:this.$store.state.signup.currentEventId, user:this.user});
        },
        watch: {
            $route (){
                // clear alert on location change
                this.clearAlert();
            }
        }
    };
</script>
