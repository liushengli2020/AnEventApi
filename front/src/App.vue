<template>
  <div class="jumbotron">
    <div class="container-fluid">
      <div class="row">

          <AccountBar/>
          <AlertBar/>
          <router-view></router-view>

      </div>
    </div>
  </div>
</template>

<script>
import AccountBar from './components/AccountBar';
import AlertBar from './components/AlertBar';
import EventList from './components/EventList';

export default {
  name: 'App',
  components: {
    AccountBar,
    AlertBar,
  },
  data: () => ({
    //
  }),
};
</script>
