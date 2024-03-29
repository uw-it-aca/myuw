<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-12 col-sm-4 px-0">
          <div class="d-flex">
            <!-- A linked secondary section -->
            <font-awesome-icon
              :icon="faSquareFull"
              :class="`text-c${section.color_id}`"
              class="my-auto me-1"
              size="xs"
            />
            <div>
            <h4
              class="myuw-text-md myuw-font-encode-sans d-inline"
              :aria-label="section.lable"
            >
              <a v-if="section.mini_card"
                v-inner="'View Mini-card'"
                :href="`/teaching/${section.href}`"
                :future-nav-target="section.navtarget"
                :title="`View mini-card of ${section.label} on Teaching page`"
              >
                {{ section.section_id }}
              </a>
              <a v-else
                :href="`/teaching/${section.href}`"
                :future-nav-target="section.navtarget"
                :title="`Pin mini-card of ${section.label} onto Teaching page`"
                @click="miniCard"
              >
                {{ section.section_id }}
              </a>
            </h4>
            </div>
            <div v-if="section.sln" class="ms-2">
              <h5 class="visually-hidden">
                Section SLN:
              </h5>
              <span>
                <a
                  v-out="'Time Schedule for SLN'"
                  :href="getTimeScheHref(section)"
                  :title="`Time Schedule for SLN ${section.sln}`"
                  target="_blank"
                  class="text-muted myuw-text-sm"
                >
                  {{ section.sln }}
                </a>
              </span>
            </div>
            <div
              class="flex-fill"
              :class="[$mq === 'mobile' ? 'ms-2' : 'text-center']"
            >
              <h5 class="visually-hidden">
                Section Type:
              </h5>
              <span class="text-capitalize myuw-text-md">
                {{ shortenType(section.section_type) }}
              </span>
            </div>
          </div>
        </div>
        <div class="col-8 col-sm-5 px-0">
          <div class="d-flex">
            <div class="flex-fill">
              <h5 class="visually-hidden">
                Section Meetings:
              </h5>
              <uw-meeting-info :section="section" no-heading />
            </div>
          </div>
        </div>
        <div class="col-2 col-sm-2 px-0">
          <h5 class="visually-hidden">
            Section Enrollments:
          </h5>
          <uw-enrollment :section="section"
            class="myuw-text-md text-nowrap"
            :class="$mq === 'desktop' ? 'ms-2' : 'ms-1'"
          />
        </div>
        <div class="col-2 col-sm-1 px-0">
          <div class="d-inline-block float-end">
            <button v-if="!section.mini_card"
              :title="`Pin mini-card of ${section.label} onto Teaching page`"
              type="button" class="btn btn-link myuw-text-md text-muted p-0 ms-1"
              @click="miniCard"
            >
              Pin
            </button>
            <button v-else
              :title="`Remove mini-card of ${section.label} from Teaching page`"
              type="button" class="btn btn-link myuw-text-md text-muted p-0 ms-1"
              @click="miniCard"
            >
              Unpin
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';
import {mapActions} from 'vuex';

import MeetingInfo from '../meeting/schedule.vue';
import Enrollment from './enrollment.vue';

export default {
  components: {
    'uw-meeting-info': MeetingInfo,
    'uw-enrollment': Enrollment,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      faSquareFull,
    };
  },
  methods: {
    ...mapActions('inst_schedule', [
      'toggleMini',
    ]),
    shortenType(str) {
      return str.length > 4 ? str.substring(0, 3) : str;
    },
    miniCard() {
      // MUWM-5320: start toggleMini first, otherwise request aborted on Firefox
      this.toggleMini(this.section);
      if (!this.section.mini_card) {
        this.$logger.cardPin(this, this.section.apiTag);
      } else {
        this.$logger.cardUnPin(this, this.section.apiTag);
      }
      if (!this.section.mini_card) {
        const targetId = this.section.anchor;
        if (window.location.pathname.startsWith('/teaching/')) {
          const targetUrl = `/teaching/${this.section.href}`;
          window.history.replaceState({}, null, targetUrl);
          this.$nextTick(() => {
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
              // wait for 100ms before anchoring on the mini card
              setTimeout(() => {
                targetElement.scrollIntoView({behavior: 'smooth'});
              }, 100);
            }
          });
        } else {
          // MUWM-5320: wait for 100ms before navigating away from the home page
          setTimeout(() => {
            window.location.href = `/teaching/${this.section.href}`;
          }, 100);
        }
      } else {
        // on Teaching page, anchor to the card
        window.history.replaceState({}, null, window.location.pathname);
      }
    }
  }
};
</script>
