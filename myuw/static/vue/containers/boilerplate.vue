<template>
  <div>
    <header>
      <div
        v-if="disableActions"
        id="actions_disabled_banner"
      >
        <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>.
        Overriding is read-only and no actions will be saved. &nbsp;&nbsp;
        <a
          href="/support/"
          style="font-weight: normal; color: #003399;"
        >
          Back to MyUW Support tool
        </a>
      </div>

      <b-collapse
        id="app_search"
        class="myuw-search"
      >
        this is search
      </b-collapse>

      <div class="myuw-thin-bar">
        <b-container
          fluid="xl"
          class="px-3"
        >
          <b-row>
            <b-col xs="2">
              <b-link
                href="/profile/"
                class="text-white"
              >
                <font-awesome-icon
                  :icon="['fas', 'user']"
                  class="mr-2"
                />{{ user.netid }}
              </b-link>
            </b-col>
            <b-col
              xs="10"
              class="text-right"
            >
              <b-link
                v-if="user.email_error"
                href="https://itconnect.uw.edu/connect/email/"
                class="ml-2 text-white"
                title="UW email services"
              >
                <font-awesome-icon
                  :icon="['fas', 'exclamation-triangle']"
                  class="mr-1"
                />Email error
              </b-link>
              <b-link
                v-else
                href="user.email_forward_url"
                class="ml-2 text-white"
                title="Open your email in new tab"
              >
                <font-awesome-icon
                  :icon="['fas', 'envelope']"
                  class="mr-1"
                />Email
              </b-link>
              <b-link
                v-b-toggle.app_search
                href="#"
                class="ml-2 text-white"
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
                class="d-none d-lg-inline ml-2 text-white"
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

      <div class="myuw-brand">
        <b-container
          fluid="xl"
          class="px-3 myuw-brand-logo"
        >
          <b-button
            v-b-toggle.nav-collapse
            variant="link"
            size="sm"
            class="d-lg-none p-0 text-white"
          >
            <font-awesome-layers class="fa-2x">
              <font-awesome-icon
                :icon="['far', 'square']"
                class="m-0"
              />
              <font-awesome-icon
                :icon="['fas', 'bars']"
                transform="shrink-8"
                class="m-0"
              />
            </font-awesome-layers>
          </b-button>
          <h2
            class="d-inline align-middle text-white"
            :class="[$mq == 'desktop' ? 'h3' : 'h5']"
          >
            MyUW <span class="sr-only">Home</span>
          </h2>
        </b-container>
      </div>
    </header>

    <div class="pt-4 pb-4 myuw-body">
      <b-container
        fluid="xl"
        class="px-3"
      >
        <b-row>
          <b-col lg="2">
            <!-- main sidebar navigation -->
            <b-collapse
              id="nav-collapse"
              class="myuw-navigation"
              role="navigation"
              :visible="$mq == 'desktop'"
            >
              <b-nav
                vertical
                :class="[$mq == 'desktop' ? '' : 'border-bottom mb-3']"
              >
                <b-nav-item
                  class="mb-2"
                  href="/"
                  :active="pageTitle == 'Home'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['fas', 'home']"
                    class="mr-2"
                  />Home
                </b-nav-item>
                <b-nav-item
                  v-if="user.affiliations.undergrad &&
                    user.affiliations.seattle ||
                    user.affiliations.hxt_viewer"
                  class="mb-2"
                  href="/husky_exp/"
                  :active="pageTitle == 'Husky Experience'"
                  :link-classes="'text-dark d-block px-2 py-1'"
                >
                  <font-awesome-icon
                    :icon="['fas', 'paw']"
                    class="mr-2"
                  />Husky Experience
                </b-nav-item>
                <b-nav-item
                  v-if="user.affiliations.student ||
                    user.affiliations.applicant"
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
                  v-if="user.affiliations.instructor"
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
                  v-if="user.affiliations.student"
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
                  <hr class="m-0">
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
            </b-collapse>
          </b-col>
          <b-col lg="10">
            <h2 :class="[pageTitle == 'Home' ? 'sr-only' : '']">
              {{ pageTitle }}
            </h2>

            <!-- page content inserted here -->
            <slot />
          </b-col>
        </b-row>
      </b-container>
    </div>

    <footer class="pt-3 pb-3 myuw-footer">
      <b-container
        fluid="xl"
        class="px-3"
      >
        <ul class="list-inline m-0">
          <li class="list-inline-item mr-1">
            <b-link
              href="mailto:help@uw.edu?subject=
              MyUW%20Comment,%20Request,%20Suggestion&body=
              Hello,%0A%0A%3CInclude%20your%20comment%20or%20question
              %20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20$' + user.netid"
              class="text-white"
            >
              <font-awesome-icon
                :icon="['fas', 'envelope']"
                class="mr-1"
              />Contact
            </b-link>
          </li>
          <li class="list-inline-item mr-1">
            <b-link
              href="https://itconnect.uw.edu/learn/tools/myuw-help-center/"
              class="text-white"
            >
              MyUW Help
            </b-link>
          </li>
          <li class="list-inline-item mr-1 d-lg-none">
            <b-link
              href="/logout/"
              class="text-white"
            >
              Sign Out
            </b-link>
          </li>
          <li class="list-inline-item mr-1">
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

        <div class="text-white-50">
          &copy; {{ new Date().getFullYear() }} University of Washington
        </div>
      </b-container>
    </footer>
  </div>
</template>

<script>
import {mapState} from 'vuex';


export default {
  components: {},
  props: {
    logoutUrl: {
      type: String,
      default: '/logout',
    },
  },
  data() {
    return {
      selectedMenu: '',
    };
  },
  computed: mapState({
    user: (state) => state.user,
    staticUrl: (state) => state.staticUrl,
    pageTitle: (state) => state.pageTitle,
    disableActions: (state) => state.disableActions,
  }),
};
</script>

<style lang="scss">

// global styles
body { min-width: 320px; }

// boilerplate
.myuw-search {
  background: red;
}
.myuw-thin-bar {
  background: #452a78;
  line-height: 40px;
  font-size: .85rem;
  white-space: nowrap;
}

.myuw-brand {
  background: #4b2e83;
  line-height: 65px;

  .myuw-brand-logo {
    background-repeat: no-repeat;
    background-size: 45px;
    background-position: right 20px bottom;
    background-image: url(../../images/w-logo-white.png);
  }

}

.myuw-navigation {
  white-space: nowrap;

  a {

    &:hover, &:focus {
      background: #ddd;
      text-decoration: none;
    }

    &.active {
      background: #ddd;
      color: #7b59b3 !important;
      svg { color: #452a78 !important; }
    }
  }

}

.myuw-body {
  background: #f5f5f5;
}

.myuw-footer {
  background: #333;
  font-size: .70rem;
  white-space: nowrap;

  ul {
    li {
     &:not(:last-child)::after {
       content: "·";
       color: #fff;
       margin-left: 0.5rem;
     }
    }
  }

}
</style>
