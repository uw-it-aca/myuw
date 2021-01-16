<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h3>
    </template>
    <template v-else #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Tacoma Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h3>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h4 class="h5 mb-3 text-dark-beige">
        For application status, contact the UW Tacoma Office of Registrar
      </h4>
      <b-container>
        <b-row>
          <b-col>Email</b-col>
          <b-col><a href="mailto:reguwt@uw.edu">reguwt@uw.edu</a></b-col>
        </b-row>
        <b-row>
          <b-col>Phone</b-col>
          <b-col>(253) 692-4913</b-col>
        </b-row>
        <b-row>
          <b-col>Fax</b-col>
          <b-col>(253) 692-4414</b-col>
        </b-row>
        <b-row>
          <b-col>Location</b-col>
          <b-col>MAT 253</b-col>
        </b-row>
        <b-row>
          <b-col>Mail</b-col>
          <b-col>
            University of Washington Tacoma
            <br>1900 Commerce Street
            <br>Tacoma, WA 98402-3100
          </b-col>
        </b-row>
      </b-container>
      <h4 class="h5 mb-3 text-dark-beige">
        Resources for Tacoma Applicants
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a href="http://www.tacoma.uw.edu/node/36610"
             target="_blank" aria-label="Financial Aid"
          >
            Learn all about student financial aid
          </a>
        </li>
        <li>
          <a href="http://www.tacoma.uw.edu/node/41373" target="_blank"
             aria-label="Financial aid key dates and deadlines"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
        <li>
          <a href="http://www.tacoma.uw.edu/node/41353"
             target="_blank" aria-label="UW Tacoma Academic calendars"
          >
            View the UW Tacoma Academic calendars
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <a class="btn btn-outline-secondary text-dark my-4" href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp"
         aria-label="Your application status details"
      >
        View your {{ applicantData.type }} application status
      </a>
      <h4 class="h5 mb-3 text-dark-beige">
        Resources for Tacoma Applicants
      </h4>
      <h5 class="h6">
        ADMISSIONS
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a
            href="http://www.tacoma.uw.edu/admissions/important-dates-deadlines-all-applicants"
            target="_blank"
            aria-label="UW Tacoma Admission: Important dates &amp; deadlines"
          >
            Important dates &amp; deadlines
          </a>
        </li>
      </ul>
      <h5 class="h6">
        FINANCES
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a href="http://www.tacoma.uw.edu/node/20240"
             target="_blank" aria-label="Applying for a financial Aid"
          >
            Applying for a financial Aid
          </a>
        </li>
        <li>
          <a href="http://www.tacoma.uw.edu/node/41373"
             target="_blank"
             aria-label="Financial aid key dates and deadlines"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
      </ul>
      <h5 class="h6">
        STUDENT LIFE
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a href="http://www.tacoma.uw.edu/admissions/visit"
             target="_blank" aria-label="Tacoma Campus Tours"
          >
            Plan your visit: Tacoma campus tours
          </a>
        </li>
        <li>
          <a href="http://www.tacoma.uw.edu/node/38753"
             target="_blank" aria-label="Student Housing"
          >
            Learn about student Housing
          </a>
        </li>
        <li>
          Check out
          <a
            href="http://www.tacoma.uw.edu/new-student-family-programs/new-student-family-programs"
            target="_blank" aria-label="New Student programs"
          >
            New Student programs
          </a>
          and
          <a href="http://www.tacoma.uw.edu/drsuwt"
             target="_blank"
             aria-label="Disability Resources for Students (DRS)"
          >
            Disability Resources for Students (DRS)
          </a>
        </li>
      </ul>
      <h5 class="h6">
        IF ADMITTED
      </h5>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a href="http://www.tacoma.uw.edu/admissions/i-was-admitted-now-what"
             target="_blank" aria-label="Next Steps for Admitted Students"
          >
            Next steps for Admitted students
          </a>
        </li>
        <li>
          <a href="http://www.tacoma.uw.edu/node/41496"
             target="_blank" aria-label="New Student Orientation"
          >
            Sign up for a New student orientation
          </a>
        </li>
        <li v-if="applicantData.is_international">
          <a href="http://www.tacoma.uw.edu/iss/to-do-list"
             target="_blank" aria-label="Int’l student to-do list"
          >
            View the Int’l student to-do list from International Student
            and Scholar Services (ISSS)
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
