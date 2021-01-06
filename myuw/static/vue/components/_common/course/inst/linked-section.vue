<template>
  <div>
    <!-- A linked secondary section -->
    <div>
      <div :class="`c${section.color_id}`" />
      <h4 class="h6 myuw-font-encode-sans">
        {{ section.section_id }}
      </h4>
    </div>

    <div v-if="section.sln">
      <h5 class="sr-only">
        Section SLN:
      </h5>
      <span>
        <a
          :href="getTimeScheHref(section)"
          :title="`Time Schedule for SLN ${section.sln}`"
          :data-linklabel="getTimeScheLinkLable(section)"
          target="_blank"
        >
          {{ section.sln }}
        </a>
      </span>
    </div>

    <div>
      <h5 class="sr-only">
        Section Type:
      </h5>
      <span class="text-capitalize">
        {{ section.section_type }}
      </span>
    </div>

    <div>
      <h5 class="sr-only">
        Section Meetings:
      </h5>
      <uw-meeting :section="section" />
    </div>

    <div>
      <h5 class="sr-only">
        Section Enrollments:
      </h5>
      <uw-enrollment :section="section" />
    </div>

    <div>
      <b-button v-if="!section.mini_card"
              variant="light"
              :aria-label="`Pin ${section.id} mini-card to teaching page`"
              title="Pin a mini-card onto teaching page"
              @click="miniCard"
      >
        Pin to Teaching
      </b-button>
      <b-button v-else
              variant="dark"
              :aria-label="`Remove ${section.id} mini-card from teaching page`"
              title="Remove the mini-card from teaching page"
              @click="miniCard"
      >
        Unpin
      </b-button>
    </div>
  </div>
</template>

<script>
import {mapActions} from 'vuex';

import MeetingInfo from './meeting.vue';
import Enrollment from './enrollment.vue';

export default {
  components: {
    'uw-meeting': MeetingInfo,
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
      this.toggleMini(this.section);
      if (!this.section.mini_card) {
        window.location.href = `/teaching/${this.section.href}`;
      }
    }
  }
};
</script>
