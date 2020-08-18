<template>
  <uw-card :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h3>Your Returning Student Application</h3>
    </template>
    <template v-else #card-heading>
      <h3>
        Your Seattle Application for
        {{ ucfirst(applicantData.quarter) }} {{ applicantData.year }}
      </h3>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h4>
        For application status, contact the Office of the University Registrar
      </h4>
      <b-container>
        <b-row>
          <b-col>Email</b-col>
          <b-col><a href="mailto:regoff@uw.edu">regoff@uw.edu</a></b-col>
        </b-row>
        <b-row>
          <b-col>Phone</b-col>
          <b-col>(206) 543-4000</b-col>
        </b-row>
        <b-row>
          <b-col>Location</b-col>
          <b-col>225 Schmitz Hall</b-col>
        </b-row>
      </b-container>

      <h4>Registration for Returning Student</h4>
      <p>
        You must confirm your intent to attend prior to being able to register.
      </p>
      <p>
        You may register during the Registration Period II of your
        quarter of readmittance. Check dates in the
        <a href="http://www.washington.edu/students/reg/calendar.html"
           target="_blank" aria-label="UW Academic calendars"
        >Academic calendar</a>.
      </p>

      <h4>Resources for Seattle Applicants</h4>
      <ul>
        <li>
          <a
            href="https://www.washington.edu/financialaid/"
            target="_blank" aria-label="Student Financial Aid"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li>
          <a href="http://www.washington.edu/students/"
             target="_blank" aria-label="Student Guide"
          >
            Check out the Student guide for academics, student life, and more
          </a>
        </li>
        <li>
          <a href="http://www.washington.edu/students/reg/calendar.html"
             target="_blank" aria-label="UW Academic calendars"
          >
            View the UW Academic calendars
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <a href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp"
         aria-label="Your application status details"
      >
        View your {{ applicantData.type }} application status
      </a>

      <h4>Resources for Seattle Applicants</h4>
      <h5>ADMISSIONS</h5>
      <ul>
        <li v-if="applicantData.is_freshman">
          <a href="https://admit.washington.edu/apply/dates-deadlines/"
             target="_blank" aria-label="Key dates &amp; deadlines for freshmen"
          >
            Key dates &amp; deadlines for freshmen
          </a>
        </li>
        <li v-if="applicantData.is_transfer">
          <a
            href="https://admit.washington.edu/apply/dates-deadlines/#transfer"
            target="_blank" aria-label="Key dates &amp; deadlines for Transfer"
          >
            Key dates &amp; deadlines for Transfer
          </a>
        </li>
        <li v-if="applicantData.if_post_bac">
          <a href="https://admit.washington.edu/apply/dates-deadlines/#postbac"
             target="_blank"
             aria-label="Key dates &amp; deadlines for Postbaccalaureate"
          >
            Key dates &amp; deadlines for Postbaccalaureate
          </a>
        </li>
      </ul>

      <h5>FINANCES</h5>
      <ul>
        <li>
          <a href="https://www.washington.edu/financialaid/"
             target="_blank" aria-label="Student Financial Aid"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li>
          <a href="https://admit.washington.edu/costs/coa/"
             target="_blank" aria-label="Cost of Attendance"
          >
            Refer to total cost of attendance for financial planning
          </a>
        </li>
      </ul>

      <h5>STUDENT LIFE</h5>
      <ul>
        <li>
          <a href="http://admit.washington.edu/Visit"
             target="_blank" aria-label="Seattle Campus Tours"
          >
            Plan your visit: Seattle campus tours
          </a>
        </li>
        <li>
          <a href="https://hfs.uw.edu/Live"
             target="_blank" aria-label="Seattle Campus Housing"
          >
            Learn about campus-living
          </a>
        </li>
        <li>
          <a href="http://hr.uw.edu/dso/services/matriculated-students/"
             target="_blank"
             aria-label="Student Services: Disability Resources"
          >
            Check out student services: Disability Resources
          </a>
        </li>
      </ul>
      <h5>IF ADMITTED</h5>
      <ul>
        <li>
          <a href="http://www.washington.edu/newhuskies/must-do/"
             target="_blank" aria-label="Next steps for Admitted students"
          >
            Next steps for Admitted students
          </a>
        </li>
        <li>
          <a href="http://www.washington.edu/newhuskies/must-do/#accept/"
             target="_blank" aria-label="Accept the admission offer"
          >
            Accept the admission offer and pay the New Student Enrollment
            &amp; Orientation Fee
          </a>
        </li>
        <li v-if="applicantData.is_international">
          <a href="https://iss.washington.edu/new-students/"
             target="_blank" aria-label="Int’l student checklist"
          >
            View the Int’l student checklist from International Student
            Services (ISS)
          </a>
        </li>
        <li>
          <a
            href="http://fyp.washington.edu/getting-started-at-the-university-of-washington/"
            target="_blank"
            aria-label="Register for an Advising &amp; Orientation session"
          >
            Register for an Advising &amp; Orientation session
          </a>
        </li>
        <li>
          <a
            href="http://www.washington.edu/uaa/advising/academic-planning/majors-and-minors/list-of-undergraduate-majors/"
            target="_blank" aria-label="Undergraduate Majors"
          >
            View undergraduate Majors
          </a>
        </li>
        <li>
          <a href="http://fyp.washington.edu/"
             target="_blank" aria-label="First Year Programs"
          >
            Learn about the First Year Programs
          </a>
        </li>
        <li>
          <a href="http://www.washington.edu/students/"
             target="_blank" aria-label="Student Guide"
          >
            Check out the Student guide
          </a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    applicantData: {
      type: [Object, Boolean],
      default: false,
    },
    isReady: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    ucfirst: (s) => s.replace(/^([a-z])/, (c) => c.toUpperCase()),
  },
};
</script>

<style scoped></style>
