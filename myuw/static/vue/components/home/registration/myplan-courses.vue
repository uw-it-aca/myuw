<template>
  <div>
    <h5 class="text-dark-beige">
      Your {{ nextTermQuarter }} {{ nextTermYear }} plan
    </h5>
    <div v-if="hadReadyCourses">
      <h6 class="font-weight-bold">
        Ready for registration
      </h6>
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
                    <abbr v-if="meeting.meeting_days.monday" title="Monday">
                      M
                    </abbr>
                    <abbr v-if="meeting.meeting_days.tuesday" title="Tuesday">
                      T
                    </abbr>
                    <abbr
                      v-if="meeting.meeting_days.wednesday"
                      title="Wednesday"
                    >
                      W
                    </abbr>
                    <abbr v-if="meeting.meeting_days.thursday" title="Thursday">
                      Th
                    </abbr>
                    <abbr v-if="meeting.meeting_days.friday" title="Friday">
                      F
                    </abbr>
                    <abbr v-if="meeting.meeting_days.saturday" title="Saturday">
                      Sa
                    </abbr>
                    <abbr v-if="meeting.meeting_days.sunday" title="Sunday">
                      Su
                    </abbr>
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
      <h6 class="font-weight-bold">
        Issues
      </h6>
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
          title="Edit plan to fix issues" target="_blank"
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
export default {
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
            (term) => term.quarter === this.nextTermQuarter,
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
