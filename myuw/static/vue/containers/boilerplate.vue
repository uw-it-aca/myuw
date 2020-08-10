<template>
  <div>
  
    <header>
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
              <font-awesome-icon icon="user" /> {{ user.netid }}
            </b-nav-item>
          </b-navbar-nav>
          
          <b-navbar-nav class="ml-auto">
            
            <b-nav-item
              v-if="user.email_error"
              href="https://itconnect.uw.edu/connect/email/"
              title="UW email services">
              <b-icon icon="exclamation-triangle"></b-icon> Email error
            </b-nav-item>

            <b-nav-item
              v-else
              :href="user.email_forward_url"
              title="Open your email in new tab">
              <font-awesome-icon icon="envelope" /> Email
            </b-nav-item>

            <b-nav-text v-b-toggle.app_search aria-label="Open search area">
              <font-awesome-icon icon="search" flip="horizontal" /> Search
            </b-nav-text>

            <b-nav-item :href="logout_url" class="d-none d-lg-block">
              <font-awesome-icon icon="sign-out-alt" /> Sign Out
            </b-nav-item>

          </b-navbar-nav>
        </b-navbar>
      </div>

      <div class="myuw-navigation">
        <b-navbar type="dark">
          <b-navbar-brand href="#">
            <b-button v-b-toggle.nav-collapse variant="outline-light" size="sm" class="d-lg-none">BB</b-button> MyUW
          </b-navbar-brand>
        </b-navbar>
      </div>
      
    </header>

    <b-collapse id="nav-collapse" is-nav class="d-sm-none d-lg-block">
      <ul class="list-unstyled">
        <li><font-awesome-icon icon="home" /> Home</li>
        <li><font-awesome-icon icon="paw" /> Husky Experience</li>
        <li><font-awesome-icon icon="edit" /> Teaching</li>
        <li><font-awesome-icon icon="credit-card" /> Accounts</li>
        <li><font-awesome-icon icon="user" /> Profile</li>
        <li><font-awesome-icon icon="calendar-check" /> Calendar</li>
        <li><font-awesome-icon icon="bookmark" /> Resources</li>
      </ul>  
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
import { library } from '@fortawesome/fontawesome-svg-core'

import { faUser, faEnvelope, faSearch, faSignOutAlt, faHome, faPaw, faBookmark, faCalendarCheck, faEdit, faCreditCard } from '@fortawesome/free-solid-svg-icons'
import { } from '@fortawesome/free-regular-svg-icons'

library.add(faUser)
library.add(faEnvelope)
library.add(faSearch)
library.add(faSignOutAlt)
library.add(faHome)
library.add(faPaw)
library.add(faEdit)
library.add(faCreditCard)
library.add(faCalendarCheck)
library.add(faBookmark)

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
