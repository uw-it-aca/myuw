<template>
  <div v-if="section.is_primary_section || !section.isLinkedSecondary">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12 col-sm-3 px-0">
          <div class="d-flex">
            <font-awesome-icon
              :icon="faSquareFull"
              size="sm"
              :class="`text-c${section.color_id}`"
              class="me-1 mt-1"
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
              <div :class="$mq !== 'mobile' ? 'd-block' : 'float-end'" >
                <div class="d-inline">
                  <h4 class="visually-hidden">
                    Course Mode:
                  </h4>
                  <span>
                    <uw-course-mode
                      v-if="notInPerson"
                      class="d-inline"
                      :section="section"
                      hide-info-link/>
                  </span>
                </div>
                <div class="d-inline ms-1">
                  <h4 class="visually-hidden">
                    Section Type:
                  </h4>
                  <span class="text-uppercase myuw-text-sm">
                    {{ section.section_type }}
                  </span>
                </div>
                <div v-if="section.sln" class="ms-1 d-inline">
                  <h4 class="visually-hidden">
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
        </div>
        <div class="col-9 col-sm-7 px-0">
          <div class="d-flex">
            <div class="flex-fill">
              <h4 class="visually-hidden">
                Section Meetings:
              </h4>
              <uw-meeting-info :section="section" class="myuw-text-md"/>
            </div>
          </div>
        </div>
        <div class="col-3 col-sm-2 px-0 text-end">
          <h4 class="visually-hidden">
            Section Enrollments:
          </h4>
          <uw-enrollment
            :section="section"
            class="myuw-text-md text-nowrap"
            :class="$mq === 'desktop' ? 'ms-3' : ''"
          />
        </div>
      </div>
    </div>

    <template v-if="getLinkedSections(section).length > 0">
      <div :class="$mq !== 'mobile' ? 'ms-3' : ''">
        <div class="my-2">
          <uw-collapsed-item
            :part="linkedSections"
            button-style="text-dark myuw-text-md"
            caller-id="TeachingSummary"
            display-open-close-indicator>
            <template #collapsed-body>
              <h3 class="myuw-text-md myuw-font-encode-sans pt-3">
                Linked Sections
              </h3>
              <uw-linked-section
                v-for="(sec, j) in getLinkedSections(section)"
                :key="`secondary-${section.id}-${j}`"
                :section="sec"
              />
            </template>
          </uw-collapsed-item>
         </div>
      </div>
    </template>
    <hr class="bg-secondary">
  </div>
</template>

<script>
import {
  faThumbtack,
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';
import CollapsedItem from '../../_common/collapsed-part.vue';
import CourseMode from '../../_common/course/course-mode/mode.vue';
import LinkedSection from '../../_common/course/inst/linked-section.vue';
import Enrollment from '../../_common/course/inst/enrollment.vue';
import MeetingInfo from '../../_common/course/meeting/schedule.vue';

export default {
  components: {
    'uw-collapsed-item': CollapsedItem,
    'uw-linked-section': LinkedSection,
    'uw-meeting-info': MeetingInfo,
    'uw-course-mode': CourseMode,
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
      faThumbtack,
      faSquareFull,
    };
  },
  computed: {
    notInPerson() {
      // MUWM-5210
      return (
        this.section.is_asynchronous ||
        this.section.is_synchronous ||
        this.section.is_hybrid);
    },
    linkedSections() {
      return {
        title: ("Linked Sections of " + this.section.curriculum_abbr +
                this.section.course_number + this.section.section_id),
        id: 'linked-sections-' + this.section.sln,
      };
    }
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
