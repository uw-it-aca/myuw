<template>
  <div>
    <h4 class="h6 text-dark-beige font-weight-bold">
      Your {{ nextTermQuarter }} {{ nextTermYear }} plan
    </h4>
    <div v-if="hadReadyCourses">
      <h5 class="myuw-text-md font-weight-bold">
        Ready for registration
      </h5>
      <ul class="list-unstyled m-0 myuw-text-sm">
        <li v-for="(course, i) in coursesRegistrable" :key="`course-${i}`">
          <div class="myuw-text-md m-0">
            {{ course.curriculum_abbr }} {{ course.course_number }}
          </div>
          <div class="container">
            <div v-for="section in course.sections" :key="section.id" class="row">
              <div class="col-2 myuw-text-md">
                {{section.section_id}} 
              </div>
              <div class="col">
                <uw-meeting-schedule :section="section" />
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="hadUnReadyCourses">
      <h5 class="myuw-text-md font-weight-bold">
        Issues
      </h5>
      <p class="myuw-text-md">
        The following plan items have issues you must resolve before they
        can be sent to Registration.
      </p>
      <ul class="list-unstyled myuw-text-sm">
        <li v-for="(course, i) in coursesUnRegistrable" :key="i">
          {{ course.curriculum_abbr }} {{ course.course_number }}
        </li>
      </ul>
      <div class="text-end myuw-text-sm">
        <a
          title="Edit plan to fix issues"
          :href="currentPlanData.myplan_href"
        >
          Go to your {{ nextTermQuarter }} {{ nextTermYear }}
          plan to resolve these issues
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import Schedule from '../../_common/course/meeting/schedule.vue';
export default {
  components: {
    'uw-meeting-schedule': Schedule,
  },
  props: {
    nextTermYear: {
      type: Number,
      required: true,
    },
    nextTermQuarter: {
      type: String,
      required: true,
    },
    myPlanData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    currentPlanData() {
      if (this.myPlanData && this.myPlanData.terms) {
        return this.myPlanData.terms.find(
            (term) => (
              term.quarter.toLowerCase() ===
              this.nextTermQuarter.toLowerCase()
            ),
        ) || {};
      }
      return {};
    },
    hadReadyCourses() {
      return this.currentPlanData.has_ready_courses;
    },
    hadUnReadyCourses() {
      return this.currentPlanData.has_unready_courses;
    },
    coursesRegistrable() {
      return this.currentPlanData.courses.filter(
          (c) => c.registrations_available,
      );
    },
    coursesUnRegistrable() {
      return this.currentPlanData.courses.filter(
          (c) => !c.registrations_available,
      );
    },
    courses() {
      return this.currentPlanData.courses;
    },
  },
  methods: {
    
  },
};
</script>
