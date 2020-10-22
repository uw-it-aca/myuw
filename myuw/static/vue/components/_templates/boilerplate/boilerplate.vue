<template>
  <div>
    <header v-if="!isHybrid">
      <div
        v-if="disableActions"
        id="actions_disabled_banner"
        class="bg-gold myuw-override myuw-text-md"
      >
        <b-container fluid="xl" class="py-2 text-center">
          <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>.
          Overriding is read-only and no actions will be saved.
          <a href="/support/">
            Back to MyUW Support tool
          </a>
        </b-container>
      </div>

      <b-collapse id="app_search" class="myuw-search bg-gold">
        <uw-search />
      </b-collapse>

      <div class="bg-dark-purple text-nowrap myuw-thin-bar myuw-text-xs">
        <b-container fluid="xl" class="px-3">
          <b-row>
            <b-col xs="2">
              <b-link href="/profile/"
                      class="text-white font-weight-light"
                      aria-label="View your profile"
              >
                <font-awesome-icon :icon="['fas', 'user']" class="mr-1" />
                {{ netid }}
              </b-link>
            </b-col>
            <b-col xs="10" class="text-right">
              <b-link
                v-if="emailError"
                href="https://itconnect.uw.edu/connect/email/"
                class="ml-2 text-danger font-weight-light"
                aria-label="UW email services"
              >
                <font-awesome-icon
                  :icon="['fas', 'exclamation-triangle']"
                  class="mr-1"
                />Email error
              </b-link>
              <b-link
                v-else
                :href="emailForwardUrl"
                class="ml-2 text-white font-weight-light"
                aria-label="Open your email in new tab"
              >
                <font-awesome-icon
                  :icon="['fas', 'envelope']"
                  class="mr-1"
                />Email
              </b-link>
              <b-link
                v-b-toggle.app_search
                href="#"
                class="ml-2 text-white font-weight-light"
                aria-label="Open search area"
              >
                <font-awesome-icon
                  :icon="['fas', 'search']"
                  flip="horizontal"
                  class="mr-1"
                />Search
              </b-link>
              <b-link
                href="/logout/"
                class="d-none d-lg-inline ml-2 text-white font-weight-light"
                aria-label="Sign out of MyUW"
              >
                <font-awesome-icon
                  :icon="['fas', 'sign-out-alt']"
                  class="mr-1"
                />Sign Out
              </b-link>
            </b-col>
          </b-row>
        </b-container>
      </div>

      <div class="bg-purple myuw-brand">
        <b-container fluid="xl" class="px-3 myuw-brand-logo">
          <b-button
            v-b-toggle.nav-collapse
            variant="link"
            size="sm"
            class="d-lg-none p-0 border-0 text-white"
            aria-label="Toggle Navigation Menu"
          >
            <font-awesome-layers class="fa-2x">
              <font-awesome-icon
                :icon="['far', 'square']"
                transform="right-1"
                class="m-0"
              />
              <font-awesome-icon
                :icon="['fas', 'bars']"
                transform="shrink-8 right-1 "
                class="m-0"
              />
            </font-awesome-layers>
          </b-button>
          <h1
            class="d-inline align-middle text-white"
            :class="[$mq == 'desktop' ? 'h3' : 'h5']"
          >
            MyUW <span class="sr-only">Home</span>
          </h1>
        </b-container>
      </div>
    </header>

    <div class="bg-light pt-4 pb-4 myuw-body">
      <b-container fluid="xl">
        <b-row :no-gutters="$mq !== 'desktop'">
          <b-col lg="2">
            <!-- main sidebar navigation -->
            <b-collapse
              v-if="!isHybrid"
              id="nav-collapse"
              class="text-nowrap myuw-navigation"
              role="navigation"
              :visible="$mq == 'desktop'"
            >
              <b-nav
                vertical
                :class="[$mq == 'desktop' ? '' : 'border-bottom']"
              >
                <b-nav-item
                  class="mb-2"
                  href="/"
                  :active="pageTitle == 'Home'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="['fas', 'home']" class="mr-2" />Home
                </b-nav-item>
                <b-nav-item
                  v-if="(undergrad && seattle) || hxtViewer"
                  class="mb-2"
                  href="/husky_exp/"
                  :active="pageTitle == 'Husky Experience'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="['fas', 'paw']" class="mr-2" />Husky
                  Experience
                </b-nav-item>
                <b-nav-item
                  v-if="student || applicant"
                  class="mb-2"
                  href="/academics/"
                  :active="pageTitle == 'Academics'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['fas', 'graduation-cap']"
                    class="mr-2"
                  />Academics
                </b-nav-item>
                <b-nav-item
                  v-if="instructor"
                  class="mb-2"
                  href="/teaching/"
                  :active="pageTitle == 'Teaching'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['far', 'edit']"
                    class="mr-2"
                  />Teaching
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/accounts/"
                  :active="pageTitle == 'Accounts'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['far', 'credit-card']"
                    class="mr-2"
                  />Accounts
                </b-nav-item>
                <b-nav-item
                  v-if="student"
                  class="mb-2"
                  href="/notices/"
                  :active="pageTitle == 'Notices'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['fas', 'exclamation-triangle']"
                    class="mr-2"
                  />Notices
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/profile/"
                  :active="pageTitle == 'Profile'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['fas', 'user']"
                    class="mr-2"
                  />Profile
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  role="separator"
                  disabled
                  :link-classes="'text-dark d-block p-0'"
                >
                  <hr class="m-0"><span class="sr-only">
                    Navigation separator</span>
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/academic_calendar/"
                  :active="pageTitle == 'Academic Calendar'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['far', 'calendar-check']"
                    class="mr-2"
                  />Calendar
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/resources/"
                  :active="pageTitle == 'UW Resources'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['fas', 'bookmark']"
                    class="mr-2"
                  />UW Resources
                </b-nav-item>
              </b-nav>
              <uw-welcome v-if="$mq === 'desktop'" />
            </b-collapse>
          </b-col>
          <b-col lg="10" role="main" aria-labelledby="mainHeader">
            <h2 id="mainHeader" :class="[pageTitle == 'Home' ? 'sr-only' : '']">
              {{ pageTitle }}
            </h2>
            <b-row>
              <slot name="primary" />
              <slot v-if="$mq !== 'mobile'" name="secondary" />
            </b-row>
          </b-col>
        </b-row>
      </b-container>
    </div>

    <footer v-if="!isHybrid" class="bg-dark pt-3 pb-3 myuw-footer myuw-text-xs">
      <b-container fluid="xl" class="px-3">
        <ul class="list-inline m-0">
          <li class="list-inline-item mr-0">
            <b-link :href="mailToUrl + netid" class="text-white">
              <font-awesome-icon
                :icon="['fas', 'envelope']"
                class="mr-1"
              />Contact
            </b-link>
          </li>
          <li class="list-inline-item mr-0">
            <b-link
              href="https://itconnect.uw.edu/learn/tools/myuw-help-center/"
              class="text-white"
            >
              MyUW Help
            </b-link>
          </li>
          <li class="list-inline-item mr-0 d-lg-none">
            <b-link href="/logout/" class="text-white">
              Sign Out
            </b-link>
          </li>
          <li class="list-inline-item mr-0">
            <b-link
              href="https://www.washington.edu/online/terms/"
              class="text-white"
            >
              Terms
            </b-link>
          </li>
          <li class="list-inline-item">
            <b-link
              href="https://www.washington.edu/online/privacy/"
              class="text-white"
            >
              Privacy
            </b-link>
          </li>
        </ul>

        <div class="text-white font-weight-light">
          &copy; {{ new Date().getFullYear() }} University of Washington
        </div>
      </b-container>
    </footer>
  </div>
</template>

<script>
import {mapState} from 'vuex';
import Search from './search.vue';
import Welcome from './welcome.vue';

export default {
  components: {
    'uw-search': Search,
    'uw-welcome': Welcome,
  },
  props: {
    logoutUrl: {
      type: String,
      default: '/logout',
    },
  },
  data() {
    return {
      isHybrid: navigator.userAgent.includes('MyUW_Hybrid/1.0'),
      selectedMenu: '',
      mailToUrl:
        'mailto:help@uw.edu?subject=MyUW%20Comment,%20Request,%20Suggestion&body=Hello,%0A%0A%3CInclude%20your%20comment%20or%20question%20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20',
    };
  },
  computed: mapState({
    netid: (state) => state.user.netid,
    emailError: (state) => state.user.email_error,
    emailForwardUrl: (state) => state.user.email_forward_url,
    undergrad: (state) => state.user.affiliations.undergrad,
    seattle: (state) => state.user.affiliations.seattle,
    hxtViewer: (state) => state.user.affiliations.hxt_viewer,
    student: (state) => state.user.affiliations.student,
    applicant: (state) => state.user.affiliations.applicant,
    instructor: (state) => state.user.affiliations.instructor,
    staticUrl: (state) => state.staticUrl,
    pageTitle: (state) => state.pageTitle,
    disableActions: (state) => state.disableActions,
  }),
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

// boilerplate

.myuw-override {
  a { color: darken($link-color, 12%) !important; }
}
//.myuw-search {}

.myuw-thin-bar {
  line-height: 40px;

  // override danger color to fix a11y contrast
  .text-danger, .text-danger:hover {
    color: lighten(map.get($theme-colors, "danger"), 25%) !important;
  }
}

.myuw-brand {
  line-height: 65px;

  .myuw-brand-logo {
    background-repeat: no-repeat;
    background-size: 45px;
    background-position: right 20px bottom;
    background-image: url(../../../../images/w-logo-white.png);
  }
}

.myuw-navigation {
  a {
    &:hover,
    &:focus {
      background: $gray-300;
      text-decoration: none;
    }

    &.active {
      background: $gray-300;
      color: map.get($theme-colors, "purple") !important;
      svg {
        color: map.get($theme-colors, "purple") !important;
      }
    }
  }
}

.myuw-welcome {
  background: $gray-300;
}


//.myuw-body { }

.myuw-footer {
  ul {
    li {
      &:not(:last-child)::after {
        content: "·";
        color: #fff;
        //margin-left: 0.5rem;
      }
    }
  }
}
</style>
