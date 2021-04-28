<template>
  <div v-if="section.is_primary_section || !section.isLinkedSecondary">
    <b-container fluid>
      <b-row>
        <b-col sm="4" class="px-0">
          <div class="d-flex">
            <font-awesome-icon
              :icon="faSquareFull"
              size="sm"
              :class="`text-c${section.color_id}`"
              class="mr-1 mt-1"
            />
            <div class="flex-fill">
              <h3
                class="myuw-text-md myuw-font-encode-sans d-inline text-nowrap"
                :aria-label="section.id.replace(/-/g,' ')"
              >
                <a
                  v-inner="'View inst course card'"
                  :href="`/teaching/${section.href}`"
                  :future-nav-target="section.navtarget"
                  title="Click to view the card on Teaching page"
                >
                  {{ section.curriculum_abbr }}
                  {{ section.course_number }}
                  {{ section.section_id }}
                </a>
              </h3>
              <div :class="$mq !== 'mobile' ? 'd-block' : 'float-right'">
                <div class="d-inline">
                  <h4 class="sr-only">
                    Section Type:
                  </h4>
                  <span class="text-uppercase myuw-text-sm">
                    {{ section.section_type }}
                  </span>
                </div>
                <div v-if="section.sln" class="ml-3 d-inline">
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
              </div>
            </div>
          </div>
        </b-col>
        <b-col sm="6" class="px-0">
          <div class="d-flex">
            <div class="flex-fill">
              <h4 class="sr-only">
                Section Meetings:
              </h4>
              <uw-meeting-info :section="section" class="myuw-text-md"/>
            </div>
          </div>
        </b-col>
        <b-col sm="2" class="px-0">
          <h4 class="sr-only">
            Section Enrollments:
          </h4>
          <uw-enrollment
            :section="section"
            class="myuw-text-md text-nowrap"
            :class="$mq === 'desktop' ? 'ml-3' : 'ml-2'"
          />
        </b-col>
      </b-row>
    </b-container>

    <template v-if="getLinkedSections(section).length > 0">
      <div :class="$mq !== 'mobile' ? 'ml-3' : ''">
        <b-button
          v-b-toggle="`linked-sections-${section.id}`"
          variant="link"
          class="p-0 text-dark myuw-text-md my-2"
        >
          Linked Sections of {{ section.curriculum_abbr }}
          {{ section.course_number }} {{ section.section_id }}
          <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" />
          <font-awesome-icon v-else :icon="faChevronUp" />
        </b-button>

        <b-collapse :id="`linked-sections-${section.id}`" v-model="isOpen">
          <uw-linked-section
            v-for="(sec, j) in getLinkedSections(section)"
            :key="`secondary-${section.id}-${j}`"
            :section="sec"
          />
        </b-collapse>
      </div>
    </template>
    <hr>
  </div>
</template>

<script>
import {
  faThumbtack,
  faChevronUp,
  faChevronDown,
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';
import LinkedSection from '../../_common/course/inst/linked-section.vue';
import Enrollment from '../../_common/course/inst/enrollment.vue';
import MeetingInfo from '../../_common/course/meeting/schedule.vue';

export default {
  components: {
    'uw-linked-section': LinkedSection,
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
      isOpen: false,
      faThumbtack,
      faChevronUp,
      faChevronDown,
      faSquareFull,
    };
  },
  methods: {
    getLinkedSections(pSection) {
      return this.$parent.sections.filter(
        (section) => (!section.is_primary_section &&
          section.primary_section_label === pSection.section_label),
      );
    },
  },
};
</script>
