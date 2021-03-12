<template>
  <div>
    <div class="d-flex">
      <!-- A linked secondary section -->
      <div>
        <div :class="`c${section.color_id}`" />
        <h4 class="h5 myuw-font-encode-sans">
          <a v-if="section.mini_card"
            :href="`/teaching/${section.href}`"
            :future-nav-target="section.navtarget"
            title="Click to view the mini-card on Teaching page"
          >
            {{ section.section_id }}
          </a>
          <a v-else
            :href="`/teaching/${section.href}`"
            :future-nav-target="section.navtarget"
            title="Click to pin the mini-card onto Teaching page"
            @click="miniCard"
          >
            {{ section.section_id }}
          </a>
        </h4>
      </div>
      <div v-if="section.sln">
        <h5 class="sr-only">
          Section SLN:
        </h5>
        <span>
          <a
            v-out="getTimeScheLinkLable(section)"
            :href="getTimeScheHref(section)"
            :title="`Time Schedule for SLN ${section.sln}`"
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

      <div class="flex-fill">
        <h5 class="sr-only">
          Section Meetings:
        </h5>
        <uw-meeting-info :section="section" />
      </div>

      <div>
        <h5 class="sr-only">
          Section Enrollments:
        </h5>
        <uw-enrollment :section="section" />
      </div>
    </div>

    <div>
      <b-button v-if="!section.mini_card"
              variant="light"
              :label="`Pin ${section.id} mini-card to teaching page`"
              title="Click to pin the mini-card onto Teaching page"
              @click="miniCard"
      >
        Pin to Teaching
      </b-button>
      <b-button v-else
              variant="dark"
              :label="`Remove ${section.id} mini-card from teaching page`"
              title="Click to remove the mini-card from Teaching page"
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
        this.$nextTick(() => {
          window.history.replaceState({}, null, `/teaching/${this.section.href}`);
          setTimeout(() => {
            document.getElementById(this.section.anchor)
              .scrollIntoView({behavior: 'smooth'});
          }, 100);
        });
      } else {
        window.history.replaceState({}, null, window.location.pathname);
      }
    }
  }
};
</script>
