<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h3>
    </template>
    <template v-else #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Seattle Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h3>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h4 class="h5 mb-3 text-dark-beige">
        For application status, contact the Office of the University Registrar
      </h4>
      <b-container>
        <b-row>
          <b-col>Email</b-col>
          <b-col><a v-out="'Contact Registrar Office'"
                   href="mailto:regoff@uw.edu">regoff@uw.edu</a></b-col>
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

      <h4 class="h5 mb-3 text-dark-beige">
        Registration for Returning Student
      </h4>
      <p>
        You must confirm your intent to attend prior to being able to register.
      </p>
      <p>
        You may register during the Registration Period II of your
        quarter of readmittance. Check dates in the
        <a href="http://www.washington.edu/students/reg/calendar.html"
           target="_blank"
        >Academic calendar</a>.
      </p>

      <h4 class="h5 mb-3 text-dark-beige">
        Resources for Seattle Applicants
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a
            v-out="'Student Financial Aid'"
            href="https://www.washington.edu/financialaid/" target="_blank"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li>
          <a v-out="'Student Guide'"
             href="http://www.washington.edu/students/" target="_blank"
          >
            Check out the Student guide for academics, student life, and more
          </a>
        </li>
        <li>
          <a v-out="'UW Academic calendars'"
             href="http://www.washington.edu/students/reg/calendar.html" target="_blank"
          >
            View the UW Academic calendars
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <a v-out="'Your application status details'"
         class="btn btn-outline-secondary text-dark my-4"
         href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp"
      >
        View your {{ applicantData.type }} application status
      </a>

      <h4 class="h5 mb-3 text-dark-beige">
        Resources for Seattle Applicants
      </h4>
      <h5 class="h6">
        ADMISSIONS
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li v-if="applicantData.is_freshman">
          <a v-out="'Key dates deadlines for freshmen'"
             href="https://admit.washington.edu/apply/dates-deadlines/" target="_blank"
          >
            Key dates &amp; deadlines for freshmen
          </a>
        </li>
        <li v-if="applicantData.is_transfer">
          <a
            v-out="'Key dates deadlines for Transfer'"
            href="https://admit.washington.edu/apply/dates-deadlines/#transfer" target="_blank"
          >
            Key dates &amp; deadlines for Transfer
          </a>
        </li>
        <li v-if="applicantData.if_post_bac">
          <a v-out="'Key dates deadlines for Postbaccalaureate'"
             href="https://admit.washington.edu/apply/dates-deadlines/#postbac"
             target="_blank"
          >
            Key dates &amp; deadlines for Postbaccalaureate
          </a>
        </li>
      </ul>

      <h5 class="h6">
        FINANCES
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'Student Financial Aid'"
             href="https://www.washington.edu/financialaid/" target="_blank"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li>
          <a v-out="'Cost of Attendance'"
             href="https://admit.washington.edu/costs/coa/" target="_blank"
          >
            Refer to total cost of attendance for financial planning
          </a>
        </li>
      </ul>

      <h5 class="h6">
        STUDENT LIFE
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'Seattle Campus Tours'"
             href="http://admit.washington.edu/Visit" target="_blank"
          >
            Plan your visit: Seattle campus tours
          </a>
        </li>
        <li>
          <a v-out="'Seattle Campus Housing'"
             href="https://hfs.uw.edu/Live" target="_blank"
          >
            Learn about campus-living
          </a>
        </li>
        <li>
          <a v-out="'Student Services: Disability Resources'"
             href="http://hr.uw.edu/dso/services/matriculated-students/"
             target="_blank"
          >
            Check out student services: Disability Resources
          </a>
        </li>
      </ul>
      <h5 class="h6">
        IF ADMITTED
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'Next steps for Admitted students'"
             href="http://www.washington.edu/newhuskies/must-do/" target="_blank"
          >
            Next steps for Admitted students
          </a>
        </li>
        <li>
          <a v-out="'Accept admission offer'"
             href="http://www.washington.edu/newhuskies/must-do/#accept/" target="_blank"
          >
            Accept the admission offer and pay the New Student Enrollment
            &amp; Orientation Fee
          </a>
        </li>
        <li v-if="applicantData.is_international">
          <a v-out="'Intl student checklist'"
             href="https://iss.washington.edu/new-students/" target="_blank"
          >
            View the Int’l student checklist from International Student
            Services (ISS)
          </a>
        </li>
        <li>
          <a
            v-out="'Register for an Advising &amp; Orientation session'"
            href="http://fyp.washington.edu/getting-started-at-the-university-of-washington/"
            target="_blank"
          >
            Register for an Advising &amp; Orientation session
          </a>
        </li>
        <li>
          <a
            v-out="'Undergraduate Majors'"
            href="http://www.washington.edu/uaa/advising/academic-planning/majors-and-minors/list-of-undergraduate-majors/" target="_blank"
          >
            View undergraduate Majors
          </a>
        </li>
        <li>
          <a v-out="'First Year Programs'"
             href="http://fyp.washington.edu/" target="_blank"
          >
            Learn about the First Year Programs
          </a>
        </li>
        <li>
          <a v-out="'Student Guide'"
             href="http://www.washington.edu/students/" target="_blank"
          >
            Check out the Student guide
          </a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';

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
};
</script>
