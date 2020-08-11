<template>
  <div>
    <header>
      <div id="actions_disabled_banner" v-if="disable_actions">
        <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>.
        Overriding is read-only and no actions will be saved. &nbsp;&nbsp;
        <a href="/support" style="font-weight: normal; color: #003399;">
          Back to MyUW Support tool
        </a>
      </div>

      <b-collapse id="app_search" class="myuw-search">
        this is search
      </b-collapse>

      <div class="myuw-thin-bar">

        <b-container fluid="lg">

          <b-link href="/profile/"><font-awesome-icon icon="user" /> {{ user.netid }}</b-link>

          <b-link v-if="user.email_error" href="https://itconnect.uw.edu/connect/email/"  title="UW email services">
            <font-awesome-icon icon="exclamation-triangle" /> Email error
          </b-link>
          <b-link v-else href="user.email_forward_url" title="Open your email in new tab">
            <font-awesome-icon icon="envelope" /> Email 
          </b-link>
          
          <b-link href="#" v-b-toggle.app_search aria-label="Open search area">
            <font-awesome-icon icon="search" flip="horizontal" /> Search
          </b-link>

          <b-link href="logout_url" class="d-none d-lg-inline">
            <font-awesome-icon icon="sign-out-alt" /> Sign Out
          </b-link>
       
        </b-container>
      </div>

      <div class="myuw-navigation">
        <b-container fluid="lg" class="myuw-brand" style="background-image: url(/static/images/w-logo-white.png)">
          <b-button v-b-toggle.nav-collapse variant="outline-light" size="sm" class="d-lg-none">=</b-button> 
          <h2 class="d-inline h3 align-middle text-white">MyUW <span class="sr-only">Home</span></h2>
        </b-container>
      </div>
    </header>

    <b-container fluid="lg">
      <b-row>
        <b-col lg="2">

          <!-- main sidebar navigation -->
          <mq-layout :mq="['mobile', 'tablet']">
            <b-collapse id="nav-collapse" is-nav>
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
          </mq-layout>
          <mq-layout mq="desktop">
            <b-collapse id="nav-collapse" is-nav visible>
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
          </mq-layout>
        
        </b-col>
        <b-col lg="10">
          
          <!-- page content inserted here -->
          <slot></slot>

        </b-col>
      </b-row>
    </b-container>

    <footer class="myuw-footer">
      <b-container fluid="lg">

        <b-link href="'mailto:help@uw.edu?subject=MyUW%20Comment,%20Request,%20Suggestion&body=Hello,%0A%0A%3CInclude%20your%20comment%20or%20question%20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20$' + user.netid"><font-awesome-icon icon="envelope" /> Contact</b-link>
        <b-link href="https://itconnect.uw.edu/learn/tools/myuw-help-center/">MyUW Help</b-link>
        <b-link href="#foo">Sign Out</b-link>
        <b-link href="#foo">Terms</b-link>
        <b-link href="#foo">Privacy</b-link>

        <p>&copy; {{ new Date().getFullYear() }} University of Washington</p>
      </b-container>
    </footer>
  </div>
</template>

<script>
import { mapState } from 'vuex';


export default {
  components: {},
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
    user: (state) => state.user,
  }),
};
</script>

<style lang="scss" scoped>

.myuw-search {
  background: red;
}
.myuw-thin-bar {
  background: #452a78;
  line-height: 40px;
}

.myuw-navigation {
  background: #4b2e83;
  line-height: 65px;

  .myuw-brand {
    //background-image: url('./../static/images/w-logo-white.png');
    background-repeat: no-repeat;
    background-size: 45px;
    background-position: right 20px bottom;
  }

}

.myuw-footer {
  background: #333;
}
</style>

<style></style>
