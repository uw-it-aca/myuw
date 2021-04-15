<template>
  <div class="d-flex">
    <!-- A linked secondary section -->
    <div class="w-15 flex-fill">
      <div :class="`c${section.color_id}`" />
      <h3 class="h6 myuw-font-encode-sans" :aria-label="section.lable">
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
      <div v-if="section.sln">
        <h4 class="sr-only">
          Section SLN:
        </h4>
        <a
          v-out="'Time Schedule for SLN'"
          :href="getTimeScheHref(section)"
          :title="`Time Schedule for SLN ${section.sln}`"
        >
          {{ section.sln }}
        </a>
      </div>
      <div>
        <h4 class="sr-only">
          Section Type:
        </h4>
        <span class="text-capitalize">
          {{ section.section_type }}
        </span>
      </div>
    </div>

    <div class="w-60 flex-fill">
      <h4 class="sr-only">
        Section Meetings:
      </h4>
      <uw-meeting-info :section="section" no-heading />
    </div>

    <div class="w-15 ml-3 flex-fill">
      <h4 class="sr-only">
        Section Enrollments:
      </h4>
      <uw-enrollment :section="section" />
    </div>

    <div class="w-10">
      <b-button v-if="!section.mini_card"
        variant="link"
        :title="`Pin mini-card of ${section.label} onto Teaching page`"
        @click="miniCard"
      >
        Pin
      </b-button>
      <b-button v-else
        variant="link"
        :title="`Remove mini-card of ${section.label} from Teaching page`"
        @click="miniCard"
      >
        Unpin
      </b-button>
    </div>
  </div>
</template>

<script>
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
