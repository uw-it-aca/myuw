<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h2 class="h3 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h2>
    </template>
    <template v-else #card-heading>
      <h2 class="h3 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Tacoma Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h2>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h3 class="h4 mb-3 text-dark-beige">
        For application status, contact the UW Tacoma Office of Registrar
      </h3>
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
      <h3 class="h4 mb-3 text-dark-beige">
        Resources for Tacoma Applicants
      </h3>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'UW Tacoma Financial Aid'"
             href="http://www.tacoma.uw.edu/node/36610" target="_blank"
          >
            Learn all about student financial aid
          </a>
        </li>
        <li>
          <a v-out="'UW Tacoma Financial aid key dates and deadlines'" href="http://www.tacoma.uw.edu/node/41373"
             target="_blank"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
        <li>
          <a v-out="'UW Tacoma Academic calendars'"
             href="http://www.tacoma.uw.edu/node/41353" target="_blank"
          >
            View the UW Tacoma Academic calendars
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
      <h3 class="h4 mb-3 text-dark-beige">
        Resources for Tacoma Applicants
      </h3>
      <h4 class="h5">
        ADMISSIONS
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a
            v-out="'UW Tacoma Admission: Important dates &amp; deadlines'"
            href="http://www.tacoma.uw.edu/admissions/important-dates-deadlines-all-applicants"
            target="_blank"
          >
            Important dates &amp; deadlines
          </a>
        </li>
      </ul>
      <h4 class="h5">
        FINANCES
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'Applying for financial Aid'"
             href="http://www.tacoma.uw.edu/node/20240" target="_blank"
          >
            Applying for a financial Aid
          </a>
        </li>
        <li>
          <a v-out="'Financial aid key dates and deadlines'"
             href="http://www.tacoma.uw.edu/node/41373"
             target="_blank"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
      </ul>
      <h4 class="h5">
        STUDENT LIFE
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'UW Tacoma Campus Tours'"
             href="http://www.tacoma.uw.edu/admissions/visit" target="_blank"
          >
            Plan your visit: Tacoma campus tours
          </a>
        </li>
        <li>
          <a v-out="'UW Tacoma Student Housing'"
             href="http://www.tacoma.uw.edu/node/38753" target="_blank"
          >
            Learn about student Housing
          </a>
        </li>
        <li>
          Check out
          <a
            v-out="'UW Tacoma New Student programs'"
            href="http://www.tacoma.uw.edu/new-student-family-programs/new-student-family-programs" target="_blank"
          >
            New Student programs
          </a>
          and
          <a v-out="'UW Tacoma Disability Resources for Students (DRS)'"
             href="http://www.tacoma.uw.edu/drsuwt"
             target="_blank"
          >
            Disability Resources for Students (DRS)
          </a>
        </li>
      </ul>
      <h4 class="h5">
        IF ADMITTED
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a v-out="'Next Steps for Admitted UW Tacoma Students'"
             href="http://www.tacoma.uw.edu/admissions/i-was-admitted-now-what" target="_blank"
          >
            Next steps for Admitted students
          </a>
        </li>
        <li>
          <a v-out="'New UW Tacoma Student Orientation'"
             href="http://www.tacoma.uw.edu/node/41496" target="_blank"
          >
            Sign up for a New student orientation
          </a>
        </li>
        <li v-if="applicantData.is_international">
          <a v-out="'UW Tacoma Intl student to-do list'"
             href="http://www.tacoma.uw.edu/iss/to-do-list" target="_blank"
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
