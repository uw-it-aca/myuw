<template>
  <div class="bg-light d-flex align-items-end flex-column" style="min-height: 100vh">
    <header v-if="!displayHybrid" class="w-100">
      <div
        v-if="disableActions"
        id="actions_disabled_banner"
        class="bg-gold myuw-override myuw-text-md"
      >
        <b-container fluid="xl" class="py-2 text-center">
          <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>. Overriding is read-only and
          no actions will be saved.
          <a v-inner="'MyUW Support tool'" href="/support/"> Back to MyUW Support tool </a>
        </b-container>
      </div>

      <b-collapse id="app_search" class="myuw-search bg-light">
        <uw-search />
      </b-collapse>

      <div class="bg-dark-purple text-nowrap myuw-thin-bar myuw-text-xs">
        <b-container fluid="xl" class="px-3">
          <b-row>
            <b-col xs="2">
              <b-link
                v-inner="'MyUW profile page'"
                href="/profile/"
                class="text-white font-weight-light"
                title="View your profile"
              >
                <font-awesome-icon :icon="faUser" class="mr-1" />
                {{ netid }}
              </b-link>
            </b-col>
            <b-col xs="10" class="text-right">
              <b-link
                v-if="emailError"
                v-out="'UW email services'"
                href="https://itconnect.uw.edu/connect/email/"
                class="ml-2 text-danger font-weight-light"
                title="UW email services"
              >
                <font-awesome-icon :icon="faExclamationTriangle" class="mr-1" />Email error
              </b-link>
              <b-link
                v-else-if="emailForwardUrl"
                v-out="'Open your email'"
                :href="emailForwardUrl"
                class="ml-2 text-white font-weight-light"
                title="Open your email in new tab"
              >
                <font-awesome-icon :icon="faEnvelope" class="mr-1" />Email
              </b-link>
              <b-link
                v-b-toggle.app_search
                href="#"
                class="ml-2 text-white font-weight-light"
                title="Open search area"
              >
                <font-awesome-icon :icon="faSearch" flip="horizontal" class="mr-1" />Search
              </b-link>
              <b-link
                v-inner="'Sign Out'"
                href="/logout/"
                class="d-none d-lg-inline ml-2 text-white font-weight-light"
                title="Sign out of MyUW"
              >
                <font-awesome-icon :icon="faSignOutAlt" class="mr-1" />Sign Out
              </b-link>
            </b-col>
          </b-row>
        </b-container>
      </div>

      <div class="bg-purple myuw-brand">
        <b-container
          fluid="xl"
          class="px-3 myuw-brand-logo"
          :style="`background-image: url(${staticUrl}images/w-logo-white.png);`"
        >
          <b-button
            v-b-toggle.nav-collapse
            variant="link"
            size="sm"
            class="d-lg-none p-0 border-0 text-white"
            title="Toggle Navigation Menu"
          >
            <font-awesome-layers class="fa-2x">
              <font-awesome-icon :icon="faSquare" transform="right-1" class="m-0" />
              <font-awesome-icon :icon="faBars" transform="shrink-8 right-1 " class="m-0" />
            </font-awesome-layers>
          </b-button>
          <div class="d-inline align-middle text-white" :class="[$mq == 'desktop' ? 'h3' : 'h5']">
            <template v-if="$mq != 'desktop'">
              <template v-if="pageTitle == 'Home'"> MyUW </template>
              <template v-else>
                <span class="sr-only">MyUW</span>
                <span aria-hidden="true">
                  <template v-if="pageTitle.includes('Preview')"> Preview Quarter </template>
                  <template v-else-if="pageTitle.includes('Textbooks')"> Textbooks </template>
                  <template v-else>
                    {{ pageTitle }}
                  </template>
                </span>
              </template>
            </template>
            <template v-else> MyUW </template>
          </div>
        </b-container>
      </div>
    </header>

    <!-- MARK: message banner display for desktop -->
    <uw-messages v-if="$mq === 'desktop'" />

    <div class="w-100 myuw-body">
      <b-container fluid="xl">
        <b-row :no-gutters="$mq !== 'desktop'">
          <b-col v-if="!displayHybrid" lg="2">
            <!-- main sidebar navigation -->
            <b-collapse
              id="nav-collapse"
              class="pt-4 text-nowrap myuw-navigation"
              role="navigation"
              :visible="$mq == 'desktop'"
            >
              <b-nav vertical :class="[$mq == 'desktop' ? '' : 'border-bottom']">
                <b-nav-item
                  class="mb-2"
                  href="/"
                  :active="pageTitle == 'Home'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faHome" class="mr-2" />Home
                </b-nav-item>
                <b-nav-item
                  v-if="(undergrad && seattle) || hxtViewer"
                  class="mb-2"
                  href="/husky_experience/"
                  :active="pageTitle == 'Husky Experience Toolkit'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faPaw" class="mr-2" />Husky Experience
                </b-nav-item>
                <b-nav-item
                  v-if="student || applicant"
                  class="mb-2"
                  href="/academics/"
                  :active="pageTitle == 'Academics'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faGraduationCap" class="mr-2" />Academics
                </b-nav-item>
                <b-nav-item
                  v-if="instructor"
                  class="mb-2"
                  href="/teaching/"
                  :active="pageTitle == 'Teaching'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faEdit" class="mr-2" />Teaching
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/accounts/"
                  :active="pageTitle == 'Accounts'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faCreditCard" class="mr-2" />Accounts
                </b-nav-item>
                <b-nav-item
                  v-if="student"
                  class="mb-2"
                  href="/notices/"
                  :active="pageTitle == 'Notices'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faExclamationTriangle" class="mr-2" />Notices
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/profile/"
                  :active="pageTitle == 'Profile'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faUser" class="mr-2" />Profile
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  role="separator"
                  disabled
                  :link-classes="'text-dark d-block p-0'"
                >
                  <hr class="m-0" />
                  <span class="sr-only"> Navigation separator</span>
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/academic_calendar/"
                  :active="pageTitle == 'Academic Calendar'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faCalendarCheck" class="mr-2" />Calendar
                </b-nav-item>
                <b-nav-item
                  class="mb-2"
                  href="/resources/"
                  :active="pageTitle == 'UW Resources'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon :icon="faBookmark" class="mr-2" />UW Resources
                </b-nav-item>
              </b-nav>
              <uw-welcome v-if="$mq === 'desktop'" />
            </b-collapse>
          </b-col>

          <b-col v-if="$mq === 'mobile' || $mq === 'tablet'" cols="12">
            <!-- MARK: message banner display for mobile and tablet -->
            <div style="margin-left: -10px; margin-right: -10px">
              <uw-messages />
            </div>
          </b-col>

          <b-col
            lg="10"
            role="main"
            aria-labelledby="mainHeader"
            :class="{'pt-4': true, 'mx-auto': displayHybrid}"
          >
            <h1
              id="mainHeader"
              class="mb-3 h3 myuw-font-encode-sans"
              :class="{
                'sr-only': pageTitle == 'Home' || pageTitle == 'Profile' ||
                  pageTitle.includes('Class of') || $mq != 'desktop',
              }"
            >
              {{ pageTitle }}
            </h1>
            <b-row>
              <slot v-if="$mq === 'mobile'" name="mobile" />
              <slot v-else name="desktop" />
            </b-row>
          </b-col>
        </b-row>
      </b-container>
    </div>

    <footer v-if="!displayHybrid" class="w-100 mt-auto bg-dark pt-3 pb-3 myuw-footer myuw-text-xs">
      <b-container fluid="xl" class="px-3">
        <ul class="list-inline m-0">
          <li class="list-inline-item mr-0">
            <b-link :href="mailToUrl + netid" class="text-white">
              <font-awesome-icon :icon="faEnvelope" class="mr-1" />Contact
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
            <b-link href="/logout/" class="text-white"> Sign Out </b-link>
          </li>
          <li class="list-inline-item mr-0">
            <b-link href="https://www.washington.edu/online/terms/" class="text-white">
              Terms
            </b-link>
          </li>
          <li class="list-inline-item">
            <b-link href="https://www.washington.edu/online/privacy/" class="text-white">
              Privacy
            </b-link>
          </li>
        </ul>

        <div class="text-white font-weight-light">
          &copy; {{ new Date().getFullYear() }} University of Washington
        </div>
      </b-container>
    </footer>
    <b-modal
      id="tourModal"
      ref="tourModal"
      dialog-class="myuw-modal"
      title="Welcome! Here's MyUW at a glance"
      title-class="text-dark-beige myuw-font-encode-sans"
      header-class="border-0"
      body-class="py-0"
      footer-class="border-0"
    >
      <img
        v-if="$mq === 'mobile' || $mq === 'tablet'"
        :src="staticUrl + 'images/myuw-tour-mobile-2.0x.png'"
        class="img-fluid"
      />
      <img v-else :src="staticUrl + 'images/myuw-tour-2.0x.png'" class="img-fluid" />
      <p class="mt-3 mb-0 myuw-text-md">
        Watch a video tour of
        <a
          v-out="'MyUW video for Instructors'"
          href="https://itconnect.uw.edu/learn/tools/myuw-help-center/myuw-instructors/"
          title="MyUW video tour for instructors"
          >MyUW for Instructors</a
        >,
        <a
          v-out="'MyUW video for staff'"
          href="https://itconnect.uw.edu/learn/tools/myuw-help-center/myuw-staff/"
          title="MyUW video tour for staff"
          >for staff</a
        >, or
        <a
          v-out="'MyUW video for students'"
          href="https://www.youtube.com/watch?v=K7GoUc32TMs&amp;t=5s&amp;list=PL-hNmjMg7KSHFdXj6yXDjZtCpjkkKBLUZ&amp;index=1"
          title="MyUW video tour for students"
          >for students</a
        >. <br /><a
          v-out="'MyUW Help Center'"
          href="https://itconnect.uw.edu/learn/tools/myuw-help-center/#annotated"
          title="MyUW Help Center in IT Connect"
          >Visit the MyUW help guide for more information</a
        >.
      </p>
      <template #modal-footer="{ hide }">
        <b-button variant="primary" size="sm" @click="hide()"> Close </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import {
  faCreditCard,
  faSquare,
  faCalendarCheck,
} from '@fortawesome/free-regular-svg-icons';

import {
  faExclamationTriangle,
  faUser,
  faEdit,
  faEnvelope,
  faSearch,
  faSignOutAlt,
  faHome,
  faGraduationCap,
  faPaw,
  faBars,
  faBookmark,
} from '@fortawesome/free-solid-svg-icons';
import { mapState, mapMutations } from 'vuex';
import axios from 'axios';
import Search from './search.vue';
import Welcome from './welcome.vue';
import Messages from './messages.vue';

export default {
  components: {
    'uw-search': Search,
    'uw-messages': Messages,
    'uw-welcome': Welcome,
  },
  props: {
    logoutUrl: {
      type: String,
      default: '/logout',
    },
    isHybrid: {
      type: String,
      required: true,
    },
    forceHybrid: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      displayHybrid: this.isHybrid === "True" || this.forceHybrid,
      selectedMenu: '',
      mailToUrl:
        'mailto:help@uw.edu?subject=MyUW%20Comment,%20Request,%20Suggestion&body=Hello,%0A%0A%3CInclude%20your%20comment%20or%20question%20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20',
      faExclamationTriangle,
      faUser,
      faEnvelope,
      faSearch,
      faSignOutAlt,
      faHome,
      faEdit,
      faCreditCard,
      faGraduationCap,
      faPaw,
      faSquare,
      faBars,
      faCalendarCheck,
      faBookmark,
    };
  },
  computed: mapState({
    netid: (state) => state.user.netid,
    emailError: (state) => state.user.email_error,
    emailForwardUrl: (state) => state.user.email_forward_url,
    affiliations: (state) => state.user.affiliations,
    undergrad: (state) => state.user.affiliations.undergrad,
    seattle: (state) => state.user.affiliations.seattle,
    hxtViewer: (state) => state.user.affiliations.hxt_viewer,
    student: (state) => state.user.affiliations.student,
    applicant: (state) => state.user.affiliations.applicant,
    instructor: (state) => state.user.affiliations.instructor,
    staticUrl: (state) => state.staticUrl,
    pageTitle: (state) => state.pageTitle,
    disableActions: (state) => state.disableActions,
    displayPopUp: (state) => state.displayPopUp,
  }),
  mounted() {
    this.$logger.setUserProperties(this.affiliations);
    this.$logger.configHybrid(this.isHybrid === "True");

    if (this.displayPopUp) {
      window.addEventListener('load', this.showTourModal);
    }
  },
  methods: {
    showTourModal: function () {
      this.$logger.onBoarding(this);
      this.$refs['tourModal'].show();
      axios
        .get('/api/v1/turn_off_tour_popup', {
          responseType: 'json',
        })
        .then((response) => {
          this.addVarToState({
            name: 'displayPopUp',
            value: false,
          });
        });
    },
    ...mapMutations(['addVarToState']),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../css/myuw/variables.scss';

// boilerplate

.myuw-override {
  a {
    color: darken($link-color, 12%) !important;
  }
}
//.myuw-search {}

.myuw-thin-bar {
  line-height: 40px;

  // override danger color to fix a11y contrast
  .text-danger,
  .text-danger:hover {
    color: lighten(map.get($theme-colors, 'danger'), 25%) !important;
  }
}

.myuw-brand {
  line-height: 65px;

  .myuw-brand-logo {
    background-repeat: no-repeat;
    background-size: 45px;
    background-position: right 20px bottom;
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
      color: map.get($theme-colors, 'purple') !important;
      svg {
        color: map.get($theme-colors, 'purple') !important;
      }
    }
  }
}

//.myuw-body { }

.myuw-footer {
  ul {
    li {
      &:not(:last-child)::after {
        content: '·';
        color: #fff;
        //margin-left: 0.5rem;
      }
    }
  }
}

::v-deep .myuw-modal {
  max-width: 600px !important;
}
</style>
