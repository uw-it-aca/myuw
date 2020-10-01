<template>
  <div>
<<<<<<< HEAD
    <h4 class="mt-4 text-dark-beige">
      Your {{ nextTermQuarter }} {{ nextTermYear }} plan
    </h4>
    <div v-if="hadReadyCourses">
      <h5 class="h6">
        Ready for registration
      </h5>
=======
    <h4 class="h6 mt-4 text-dark-beige">
      Your {{ nextTermQuarter }} {{ nextTermYear }} plan
    </h4>
    <div v-if="hadReadyCourses">
      <h5>Ready for registration</h5>
>>>>>>> Begin styling myplan course reg list.
      <ul class="list-unstyled m-0">
        <li v-for="(course, i) in coursesRegistrable" :key="`course-${i}`">
          <h6>{{ course.curriculum_abbr }} {{ course.course_number }}</h6>
          <table>
            <thead>
              <tr>
                <td>Section</td>
                <td>Day</td>
                <td>Time</td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(section, j) in course.sections" :key="`section-${j}`">
                <template
                  v-for="(meeting, k) in section.section_data.meetings"
                >
                  <td :key="`meeting-0-${k}`">
                    <span v-if="k == 0">Section </span>
                    <span v-else class="sr-only">Section </span>
                    {{ section.section_id }}
                  </td>
                  <td
                    v-if="meeting.days_tdb"
                    :key="`meeting-1-${k}`"
                    colspan="2"
                  >
                    Days and times to be arranged
                  </td>
                  <td v-else :key="`meeting-2-${k}`">
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
                  <td v-if="!meeting.days_tdb" :key="`meeting-3-${k}`">
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
      <h5 class="h6">
        Not ready for registration
      </h5>
      <ul>
        <li v-for="(course, i) in courses" :key="i">
          {{ course.curriculum_abbr }} {{ course.course_number }}
        </li>
      </ul>
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
      return this.myPlanData.terms.find(
          (term) => term.quarter === this.nextTermQuarter,
      );
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
