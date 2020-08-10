<template>
  <div>
   
   <!--<myuw-header :disable_actions="disable_actions" :logout_url="logout_url" />-->

    <div>
    <div id="actions_disabled_banner" v-if="disable_actions">
      <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>. Overriding
      is read-only and no actions will be saved. &nbsp;&nbsp;
      <a href="/support" style="font-weight: normal; color: #003399;">
        Back to MyUW Support tool
      </a>
    </div>

    <b-collapse id="app_search">
      this is search
    </b-collapse>

    <div class="myuw-thin-bar">
      <b-navbar class="p-0" type="dark">
        <b-navbar-nav>
          <b-nav-item href="/profile/">
            <b-icon icon="person-fill"></b-icon> {{ user.netid }}
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item
            v-if="user.email_error"
            href="https://itconnect.uw.edu/connect/email/"
            title="UW email services"
          >
            <b-icon icon="exclamation-triangle"></b-icon> Email error
          </b-nav-item>
          <b-nav-item
            v-else
            :href="user.email_forward_url"
            title="Open your email in new tab"
          >
            <b-icon icon="envelope-fill"></b-icon> Email
          </b-nav-item>
          <b-nav-text v-b-toggle.app_search aria-label="Open search area">
            <b-icon icon="search"></b-icon> Search
          </b-nav-text>
          <b-nav-item :href="logout_url">
            <b-icon icon="box-arrow-right"></b-icon> Sign Out
          </b-nav-item>
        </b-navbar-nav>
      </b-navbar>
    </div>

    <div class="myuw-navigation">
      <b-navbar toggleable="lg" type="dark">
        <b-navbar-brand href="#">MyUW</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      </b-navbar>
    </div>

    
    
  </div>

    <b-collapse visible id="nav-collapse" is-nav>
      main navigation
    </b-collapse>
      
    <slot></slot>
  
    <footer>
        <b-list-group horizontal>
            <b-list-group-item :href="'mailto:help@uw.edu?subject=MyUW%20Comment,%20Request,%20Suggestion&body=Hello,%0A%0A%3CInclude%20your%20comment%20or%20question%20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20$' + user.netid">
                <b-icon icon="envelope-fill"></b-icon> Contact
            </b-list-group-item>
            <b-list-group-item href="https://itconnect.uw.edu/learn/tools/myuw-help-center/">
                MyUW Help
            </b-list-group-item>
            <b-list-group-item>Sign Out</b-list-group-item>
            <b-list-group-item >Terms</b-list-group-item>
            <b-list-group-item >Privacy</b-list-group-item>
        </b-list-group>
        <span>&copy; {{(new Date()).getFullYear()}} University of Washington</span>
    </footer>

  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  components: {
  },
  props: {
    disable_actions: {
      type: Boolean,
      default: false,
    },
    logout_url: String,
  },
  data: function () {
    return {};
  },
  computed: mapState({
        user: state => state.user
    })
};
</script>

<style scoped>
.myuw-thin-bar {
  background: #452a78;
}

.myuw-navigation {
  background: #4b2e83;
}
</style>

<style>

</style>
