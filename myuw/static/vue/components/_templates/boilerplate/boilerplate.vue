<template>
  <div class="bg-light d-flex align-items-end flex-column" style="min-height: 100vh">
    <header v-if="!displayHybrid" class="w-100">
      <div
        v-if="disableActions"
        id="actions_disabled_banner"
        class="bg-gold myuw-override myuw-text-md"
      >
        <div class="container-xl py-2 text-center">
          <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>. Overriding is read-only and
          no actions will be saved.
          <a v-inner="'MyUW Support tool'" href="/support/"> Back to MyUW Support tool </a>
        </div>
      </div>

      <b-collapse id="app_search" class="myuw-search bg-light">
        <uw-search />
      </b-collapse>

      <div class="bg-dark-purple text-nowrap myuw-thin-bar myuw-text-xs">
        <div class="container-xl px-3">
          <div class="row">
            <div class="col">
              <a
                v-inner="'MyUW profile page'"
                href="/profile/"
                class="text-white font-weight-light"
                title="View your profile"
                ><font-awesome-icon :icon="faUser" class="mr-1" />{{ netid }}</a
              >
            </div>
            <div class="col text-right">
              <a
                v-if="emailError"
                v-out="'UW email services'"
                href="https://itconnect.uw.edu/connect/email/"
                class="ml-2 text-danger font-weight-light"
                title="UW email services"
                ><font-awesome-icon :icon="faExclamationTriangle" class="mr-1" />Email error</a
              >
              <a
                v-else-if="emailForwardUrl"
                v-out="'Open your email'"
                :href="emailForwardUrl"
                class="ml-2 text-white font-weight-light"
                title="Open your email"
                ><font-awesome-icon :icon="faEnvelope" class="mr-1" />Email</a
              >
              <a
                v-b-toggle.app_search
                href="#"
                class="ml-2 text-white font-weight-light"
                title="Open search panel"
                ><font-awesome-icon :icon="faSearch" flip="horizontal" class="mr-1" />Search</a
              >
              <a
                v-inner="'Sign Out'"
                href="/logout/"
                class="d-none d-lg-inline ml-2 text-white font-weight-light"
                title="Sign out of MyUW"
                ><font-awesome-icon :icon="faSignOutAlt" class="mr-1" />Sign Out</a
              >
            </div>
          </div>
        </div>
      </div>

      <div class="bg-purple myuw-brand">
        <div
          class="container-xl px-3 myuw-brand-logo"
          :style="`background-image: url(${staticUrl}images/w-logo-white.png);`"
        >
          <button
            v-b-toggle.nav-collapse
            type="button"
            class="btn btn-link btn-sm d-lg-none p-0 border-0 text-white"
            title="Toggle Navigation Menu"
          >
            <font-awesome-layers class="fa-2x">
              <font-awesome-icon :icon="faSquare" transform="right-1" class="m-0" />
              <font-awesome-icon :icon="faBars" transform="shrink-8 right-1 " class="m-0" />
            </font-awesome-layers>
          </button>
          <div
            class="myuw-title d-inline align-middle text-white"
            :class="[$mq == 'desktop' ? 'h3' : 'h5']"
          >
            <template v-if="$mq != 'desktop'">
              <template v-if="page.title == 'Home'"> MyUW </template>
              <template v-else>
                <span class="sr-only">MyUW</span>
                <span aria-hidden="true">
                  <template v-if="page.title.includes('Preview')"> Preview Quarter </template>
                  <template v-else-if="page.title.includes('Textbooks')"> Textbooks </template>
                  <template v-else>
                    {{ page.title }}
                  </template>
                </span>
              </template>
            </template>
            <template v-else>
              <a href="/">MyUW</a>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- MARK: message banner display for desktop -->
    <uw-messages v-if="$mq === 'desktop'" />

    <div class="w-100 myuw-body">
      <div class="container-xl">
        <div class="row" :no-gutters="$mq !== 'desktop'">
          <div v-if="!displayHybrid" class="col-lg-2">
            <!-- main sidebar navigation -->
            <b-collapse
              id="nav-collapse"
              class="pt-4 text-nowrap myuw-navigation"
              role="navigation"
              :visible="$mq == 'desktop'"
            >
              <div class="nav flex-column" :class="[$mq == 'desktop' ? '' : 'border-bottom']">
                <li class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/"
                    :class="{ active: page.title == 'Home' }"
                    ><font-awesome-icon :icon="faHome" class="mr-2" fixed-width />Home</a
                  >
                </li>
                <li v-if="student || applicant" class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/academics/"
                    :class="{ active: page.title == 'Academics' }"
                    ><font-awesome-icon :icon="faGraduationCap" class="mr-2" fixed-width />Academics
                  </a>
                </li>
                <li v-if="(undergrad && seattle) || hxtViewer" class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/husky_experience/"
                    :class="{ active: page.title == 'Husky Experience Toolkit' }"
                  >
                    <font-awesome-icon :icon="faPaw" class="mr-2" fixed-width />Husky Experience</a
                  >
                </li>
                <li v-if="instructor" class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/teaching/"
                    :class="{ active: page.title == 'Teaching' }"
                  >
                    <font-awesome-icon :icon="faEdit" class="mr-2" fixed-width />Teaching</a
                  >
                </li>
                <li class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/accounts/"
                    :class="{ active: page.title == 'Accounts' }"
                  >
                    <font-awesome-icon :icon="faCreditCard" class="mr-2" fixed-width />Accounts</a
                  >
                </li>
                <li v-if="student" class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/notices/"
                    :class="{ active: page.title == 'Notices' }"
                  >
                    <font-awesome-icon
                      :icon="faExclamationTriangle"
                      class="mr-2"
                      fixed-width
                    />Notices</a
                  >
                </li>
                <li class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/profile/"
                    :class="{ active: page.title == 'Profile' }"
                  >
                    <font-awesome-icon :icon="faUser" class="mr-2" fixed-width />Profile</a
                  >
                </li>
                <li class="nav-item mb-2" aria-hidden="true">
                  <a class="nav-link disabled text-dark d-block p-0 internal-link" href="#">
                    <hr class="m-0" />
                    <span class="sr-only"> Navigation separator</span></a
                  >
                </li>
                <li class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/academic_calendar/"
                    :class="{ active: page.title == 'Academic Calendar' }"
                  >
                    <font-awesome-icon
                      :icon="faCalendarCheck"
                      class="mr-2"
                      fixed-width
                    />Calendar</a
                  >
                </li>
                <li class="nav-item mb-2">
                  <a
                    class="nav-link text-dark d-block px-2 py-1"
                    href="/resources/"
                    :class="{ active: page.title == 'UW Resources' }"
                  >
                    <font-awesome-icon :icon="faBookmark" class="mr-2" fixed-width />UW Resources</a
                  >
                </li>
              </div>
            </b-collapse>
            <uw-welcome v-if="$mq === 'desktop'" />
          </div>
          <div v-if="$mq === 'mobile' || $mq === 'tablet'" class="col">
            <!-- MARK: message banner display for mobile and tablet -->
            <div style="margin-left: -10px; margin-right: -10px">
              <uw-messages />
            </div>
          </div>
          <div
            class="col-lg-10"
            role="main"
            aria-labelledby="mainHeader"
            :class="{ 'pt-4': true, 'mx-auto': displayHybrid }"
          >
            <h1
              id="mainHeader"
              class="mb-3 h3 myuw-font-encode-sans"
              :class="{ 'sr-only': page.hideTitle || $mq != 'desktop' }"
            >
              {{ page.title }}
            </h1>
            <div class="row">
              <slot v-if="$mq === 'mobile'" name="mobile" />
              <slot v-else name="desktop" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer v-if="!displayHybrid" class="w-100 mt-auto bg-dark pt-3 pb-3 myuw-footer myuw-text-xs">
      <div class="container-xl px-3">
        <ul class="list-inline mb-2">
          <li class="list-inline-item">
            <a :href="mailToUrl + netid" class="text-white mr-2">
              <font-awesome-icon :icon="faEnvelope" class="mr-1" />Contact
            </a>
          </li>
          <li class="list-inline-item">
            <a
              href="https://itconnect.uw.edu/learn/tools/myuw-help-center/"
              class="text-white mr-2"
            >
              MyUW Help
            </a>
          </li>
          <li class="list-inline-item mr-0 d-lg-none">
            <a href="/logout/" class="text-white"> Sign Out </a>
          </li>
          <li class="list-inline-item">
            <a href="https://www.washington.edu/online/terms/" class="text-white mr-2">
              Terms
            </a>
          </li>
          <li class="list-inline-item">
            <a href="https://www.washington.edu/online/privacy/" class="text-white mr-2">
              Privacy
            </a>
          </li>
        </ul>

        <div class="font-weight-light" style="color:#aaa">
          &copy; {{ new Date().getFullYear() }} University of Washington
        </div>
      </div>
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
      no-close-on-backdrop
      no-close-on-esc
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
        <button slot-scope="" type="button" class="btn btn-primary btn-sm" @click="hide()">
          Close
        </button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { faCreditCard, faSquare, faCalendarCheck } from '@fortawesome/free-regular-svg-icons';

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
      displayHybrid: this.isHybrid === 'True' || this.forceHybrid,
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
    netid: state => state.user.netid,
    emailError: state => state.user.email_error,
    emailForwardUrl: state => state.user.email_forward_url,
    affiliations: state => state.user.affiliations,
    undergrad: state => state.user.affiliations.undergrad,
    seattle: state => state.user.affiliations.seattle,
    hxtViewer: state => state.user.affiliations.hxt_viewer,
    student: state => state.user.affiliations.student,
    applicant: state => state.user.affiliations.applicant,
    instructor: state => state.user.affiliations.instructor,
    staticUrl: state => state.staticUrl,
    page: state => state.page,
    disableActions: state => state.disableActions,
    displayPopUp: state => state.displayPopUp,
  }),
  created() {
    this.$logger.setUserProperties(this.affiliations);
    this.$logger.setHybrid(this.isHybrid === 'True');
  },
  mounted() {
    if (this.displayPopUp) {
      window.addEventListener('load', this.showTourModal);
    }
  },
  methods: {
    showTourModal: function() {
      this.$logger.onBoarding(this);
      this.$refs['tourModal'].show();
      axios
        .get('/api/v1/turn_off_tour_popup', {
          responseType: 'json',
        })
        .then(response => {
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

.myuw-title {
  a,
  a:hover,
  a:focus,
  a:visited {
    color: #fff;
  }
}

::v-deep .myuw-modal {
  max-width: 600px !important;
}
</style>
