<template>
  <div>
    <div class="d-flex">
      <!-- A linked secondary section -->
      <div>
        <div :class="`c${section.color_id}`" />
        <h3
          class="h5 myuw-font-encode-sans"
          :aria-label="section.id.replace(/-/g,' ')"
        >
          <a v-if="section.mini_card"
            v-inner="'View Mini-card'"
            :href="`/teaching/${section.href}`"
            :future-nav-target="section.navtarget"
            title="View mini-card on Teaching page"
          >
            {{ section.section_id }}
          </a>
          <a v-else
            :href="`/teaching/${section.href}`"
            :future-nav-target="section.navtarget"
            :title="`Pin ${section.id} mini-card to teaching page`"
            @click="miniCard"
          >
            {{ section.section_id }}
          </a>
        </h3>
      </div>
      <div v-if="section.sln">
        <h4 class="sr-only">
          Section SLN:
        </h4>
        <span>
          <a
            v-out="'Time Schedule for SLN'"
            :href="getTimeScheHref(section)"
            :title="`Time Schedule for SLN ${section.sln}`"
            target="_blank"
          >
            {{ section.sln }}
          </a>
        </span>
      </div>
      <div>
        <h4 class="sr-only">
          Section Type:
        </h4>
        <span class="text-capitalize">
          {{ section.section_type }}
        </span>
      </div>

      <div class="flex-fill">
        <h4 class="sr-only">
          Section Meetings:
        </h4>
        <uw-meeting-info :section="section" noHeading />
      </div>

      <div>
        <h4 class="sr-only">
          Section Enrollments:
        </h4>
        <uw-enrollment :section="section" />
      </div>
    </div>

    <div>
      <b-button v-if="!section.mini_card"
        variant="light"
        :title="`Pin ${section.id} mini-card to teaching page`"
        @click="miniCard"
      >
        Pin to Teaching
      </b-button>
      <b-button v-else
        variant="dark"
        :title="`Remove ${section.id} mini-card from teaching page`"
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
          window.location.pathname = `/teaching/${this.section.href}`;
        }
      } else {
        window.history.replaceState({}, null, window.location.pathname);
      }
    }
  }
};
</script>
