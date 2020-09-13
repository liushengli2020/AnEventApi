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
                            <th scope="col" class="text-nowrap">location</th>
                            <th scope="col" class="text-nowrap">start time</th>
                            <th scope="col" class="text-nowrap">end time</th>
                            <th scope="col" class="text-nowrap" v-if="loggedIn">operation</th>
                            <th scope="col" class="text-nowrap" v-if="isAdmin">managerment</th>
                        </tr>
                        </thead>
                        <tbody v-if="events.items">
                        <tr v-for="event in events.items" :key="event.id">
                            <td class="text-nowrap">{{event.id}}</td>
                            <td class="text-nowrap">{{event.name}}</td>
                            <td class="text-nowrap">{{event.location}} </td>
                            <td class="text-nowrap">{{event.start_time}} </td>
                            <td class="text-nowrap">{{event.end_time}} </td>
                            <td class="text-nowrap" v-if="loggedIn">
                                <button class="btn btn-primary btn-sm "
                                        @click="signupEvent({eventId:event.id, userId:user.userId, user})">
                                    Sign up
                                </button>
                                <button class="btn btn-primary btn-sm ml-1"
                                        @click="quitEvent({eventId:event.id, userId:user.userId, user})" >
                                    quit
                                </button>
                            </td>
                            <td class="text-nowrap" v-if="isAdmin">
                                <div>
                                    <label for="userId">user id</label>
                                    <input type="text" id="userId"  v-model="userId" class="form-control" placeholder="user id">
                                    <button class="btn btn-primary btn-sm ml-1"
                                            @click="signupEvent({eventId:event.id, userId, user})" >
                                        Sign up Other
                                    </button>
                                </div>
                                    <button class="btn btn-primary btn-sm ml-1"
                                            @click="onSeeWho(event.id)" >
                                    See Who
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
                events: state => state.event.all,
            }),
            isAdmin () {
                return this.$store.state.account.status.isAdmin;
            },
            loggedIn () {
                return this.$store.state.account.status.loggedIn;
            },
            user () {
                return this.$store.state.account.user;
            }
        },
        methods: {
            ...mapActions('event', ['getAllEvents']),
            ...mapActions('signup', ['signupEvent','quitEvent']),
            onSeeWho(eventId){
                this.$store.state.signup.currentEventId = eventId;
                this.$router.push('event-signup');
            },
        },
        created () {
            this.getAllEvents();
        },
        watch: {
            $route (){
                // clear alert on location change
                this.clearAlert();
            }
        }
    };
</script>
