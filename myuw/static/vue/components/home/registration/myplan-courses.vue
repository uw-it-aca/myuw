<template>
  <div>
    <h4 class="text-dark-beige">
      Your {{ nextTermQuarter }} {{ nextTermYear }} plan
    </h4>
    <div v-if="hadReadyCourses">
      <h5 class="font-weight-bold">
        Ready for registration
      </h5>
      <ul class="list-unstyled m-0 myuw-text-sm">
        <li v-for="(course, i) in coursesRegistrable" :key="`course-${i}`">
          <div class="myuw-text-md m-0">
            {{ course.curriculum_abbr }} {{ course.course_number }}
          </div>
          <table class="table table-borderless table-sm myuw-text-sm">
            <thead class="sr-only">
              <tr>
                <td>Section</td>
                <td>Day</td>
                <td>Time</td>
              </tr>
            </thead>
            <tbody class="text-dark">
              <tr v-for="(section, j) in course.sections" :key="`section-${j}`">
                <template
                  v-for="(meeting, k) in section.section_data.meetings"
                >
                  <td :key="`meeting-0-${k}`" class="w-25 pl-0">
                    <span v-if="k == 0">Section </span>
                    <span v-else class="sr-only">Section </span>
                    {{ section.section_id }}
                  </td>
                  <td
                    v-if="meeting.days_tdb"
                    :key="`meeting-1-${k}`"
                    colspan="2"
                    class="w-25"
                  >
                    Days and times to be arranged
                  </td>
                  <td v-else :key="`meeting-2-${k}`" class="w-25">
                    <uw-meeting-days :meeting="meeting" />
                  </td>
                  <td v-if="!meeting.days_tdb" :key="`meeting-3-${k}`"
                      class="w-50 text-nowrap"
                  >
                    {{ meeting.start_time }} &ndash; {{ meeting.end_time }}
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </li>
      </ul>
    </div>
    <div v-if="hadUnReadyCourses">
      <h5 class="font-weight-bold">
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
      <div class="text-right myuw-text-sm">
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
import Days from '../../_common/course/meeting/days.vue';
export default {
  components: {
    'uw-meeting-days': Days,
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
};
</script>
