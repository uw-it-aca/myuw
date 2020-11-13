<template>
  <uw-card v-if="instructor && isReady" loaded>
    <template #card-heading>
      <h3>{{ ucfirst(quarter) }} {{ year }} Teaching Schedule</h3>
    </template>
    <template #card-body>
      <p v-if="!instSchedule.sections.length">
        You are not teaching any courses.
      </p>
      <div v-else>
        <uw-section
          v-for="section in instSchedule.sections"
          :key="section.id"
          :section="section"
        >
          <b-button
            v-if="!isOpen"
            v-b-toggle="`linked-sections-${section.id}`"
            variant="link"
            size="sm"
            aria-controls="`linked-sections-${section.id}`"
            aria-label="`SHOW LINKED SECTIONS for ${section.navtarget}`"
            title="Expand to show linked sections"
          >
            Show Linked Sections of {{ section.curriculum_abbr }}
            {{ section.course_number }} {{ section.section_id }}
          </b-button>
          <b-button
            v-else
            v-b-toggle="`linked-sections-${section.id}`"
            variant="link"
            size="sm"
            aria-controls="`linked-sections-${section.id}`"
            aria-label="`HIDE LINKED SECTIONS for ${section.navtarget}`"
            title="Collapse to show linked sections"
          >
            Hide Linked Sections of {{ section.curriculum_abbr }}
            {{ section.course_number }} {{ section.section_id }}
          </b-button>

          <b-collapse
            :id="`linked-sections-${section.id}`"
            v-model="isOpen"
            aria-label="`LINKED SECTIONS FOR ${section.navtarget}`"
          >
            <uw-section
              v-for="(sec, j) in getLinkedSections(section)" :key="j"
              :section="sec"
            />
          </b-collapse>
        </uw-section>
      </div>
      <div>
        <a :href="`/academic_calendar/#${year},${quarter}`">
          View {{ ucfirst(quarter) }} {{ year }} important dates
          and deadlines
        </a>
      </div>
    </template>
  </uw-card>

  <uw-card v-else-if="isErrored && statusCodeTagged(term) == 404" loaded>
    <template #card-heading>
      <h3>{{ ucfirst(quarter) }} {{ year }} Teaching Schedule</h3>
    </template>
    <template #card-body>
      <p>
        <i class="fa fa-exclamation-triangle" />
        An error occurred and MyUW cannot load your teaching schedule
        right now. In the meantime, try the
        <a
          href="https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/default.aspx"
          data-linklabel="MyClass" target="_blank"
        >
          My Class Instructor Resources
        </a> page.
      </p>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import Section from './section.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-section': Section,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    term: {
      type: String,
      default: 'current',
    },
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
      year: (state) => state.termData.year,
      quarter: (state) => state.termData.quarter,
      summerTerm: (state) => state.termData.summer_term,
    }),
    ...mapState('inst_schedule', {
      instSchedule(state) {
        return state.value[this.term];
      },
    }),
    ...mapGetters('inst_schedule', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    isReady() {
      return this.isReadyTagged(this.term);
    },
    isErrored() {
      return this.isErroredTagged(this.term);
    },
  },
  created() {
    if (this.instructor) {
      this.fetchInstSche(this.term);
    }
  },
  methods: {
    ...mapActions('inst_schedule', {
      fetchInstSche: 'fetch',
    }),
    getLinkedSections(pSection) {
      return this.instSchedule.sections.filter(
          (section) => (!section.is_primary_section &&
          section.primary_section_label === pSection.section_label),
      );
    },
  },
};
</script>
