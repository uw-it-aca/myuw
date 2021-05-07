<template>
  <div>
    <b-container fluid>
      <b-row>
        <b-col cols="12" sm="4" class="px-0">
          <div class="d-flex">
            <!-- A linked secondary section -->
            <font-awesome-icon
              :icon="faSquareFull"
              :class="`text-c${section.color_id}`"
              class="my-auto mr-1"
              size="xs"
            />
            <div>
            <h3
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
            </h3>
            </div>
            <div v-if="section.sln" class="ml-2">
              <h4 class="sr-only">
                Section SLN:
              </h4>
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
              :class="[$mq === 'mobile' ? 'ml-2' : 'text-center']"
            >
              <h4 class="sr-only">
                Section Type:
              </h4>
              <span class="text-capitalize myuw-text-md">
                {{ section.section_type }}
              </span>
            </div>
          </div>
        </b-col>
        <b-col cols="8" sm="5" class="px-0">
          <div class="d-flex">
            <div class="flex-fill">
              <h4 class="sr-only">
                Section Meetings:
              </h4>
              <uw-meeting-info :section="section" no-heading />
            </div>
          </div>
        </b-col>
        <b-col cols="2" sm="2" class="px-0">
          <h4 class="sr-only">
            Section Enrollments:
          </h4>
          <uw-enrollment :section="section"
            class="myuw-text-md text-nowrap"
            :class="$mq === 'desktop' ? 'ml-2' : 'ml-1'"
          />
        </b-col>
        <b-col cols="2" sm="1" class="px-0">
          <div class="d-inline-block float-right">
            <b-button v-if="!section.mini_card"
              variant="link"
              :title="`Pin mini-card of ${section.label} onto Teaching page`"
              class="myuw-text-md text-muted p-0 ml-1"
              @click="miniCard"
            >
              Pin
            </b-button>
            <b-button v-else
              variant="link"
              :title="`Remove mini-card of ${section.label} from Teaching page`"
              class="myuw-text-md text-muted p-0 ml-1"
              @click="miniCard"
            >
              Unpin
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
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
    miniCard() {
      if (!this.section.mini_card) {
        this.$logger.cardPin(this, this.section.apiTag);
      } else {
        this.$logger.cardUnPin(this, this.section.apiTag);
      }
      this.toggleMini(this.section);
      if (!this.section.mini_card) {
        if (window.location.pathname.startsWith('/teaching/')) {
          this.$nextTick(() => {
            window.history.replaceState({}, null, `/teaching/${this.section.href}`);
            setTimeout(() => {
              document.getElementById(this.section.anchor)
                .scrollIntoView({behavior: 'smooth'});
            }, 100);
          });
        } else {
          // from home page, go to the card on teaching page
          window.location.href = `/teaching/${this.section.href}`;
        }
      } else {
        // on Teaching page, go to the card
        window.history.replaceState({}, null, window.location.pathname);
      }
    }
  }
};
</script>
