<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h2>
    </template>
    <template v-else #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Tacoma Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h2>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h3 class="h6 myuw-font-encode-sans">
        Application status
      </h3>
      <p class="myuw-text-md">For application status, contact the UW Tacoma Office of Registrar:</p>
      <div class="container mb-3 myuw-text-md">
        <div class="row">
          <div class="col">Email</div>
          <div class="col"><a href="mailto:reguwt@uw.edu">reguwt@uw.edu</a></div>
        </div>
        <div class="row">
          <div class="col">Phone</div>
          <div class="col">(253) 692-4913</div>
        </div>
        <div class="row">
          <div class="col">Fax</div>
          <div class="col">(253) 692-4414</div>
        </div>
        <div class="row">
          <div class="col">Location</div>
          <div class="col">MAT 253</div>
        </div>
        <div class="row">
          <div class="col">Mail</div>
          <div class="col">
            University of Washington Tacoma
            <br>1900 Commerce Street
            <br>Tacoma, WA 98402-3100
          </div>
        </div>
      </div>
      <h3 class="h6 myuw-font-encode-sans">
        Resources for Tacoma applicants
      </h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'UW Tacoma financial aid'"
             href="https://www.tacoma.uw.edu/finaid/application-process"
          >
            Applying for financial aid
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'UW Tacoma financial aid key dates and deadlines'"
            href="https://www.tacoma.uw.edu/finaid/dates"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'UW Tacoma Academic Calendar'"
             href="https://www.tacoma.uw.edu/registrar/academic-calendar"
          >
           UW Tacoma Academic Calendar
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <uw-link-button class="my-4"
        href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp"
      >
        View your {{ applicantData.type }} application status
      </uw-link-button>
      <h3 class="h6 myuw-font-encode-sans">
        Resources for Tacoma applicants
      </h3>
      <h4 class="h6">
        ADMISSIONS
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a
            v-out="'UW Tacoma Admission: Important dates &amp; deadlines'"
            href="https://www.tacoma.uw.edu/admissions/important-dates"
          >
            Important dates &amp; deadlines
          </a>
        </li>
      </ul>
      <h4 class="h6">
        FINANCES
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'Applying for financial Aid'"
             href="https://www.tacoma.uw.edu/finaid/application-process"
          >
            Applying for a financial Aid
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'Financial aid key dates and deadlines'"
             href="https://www.tacoma.uw.edu/finaid/dates"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
      </ul>
      <h4 class="h6">
        STUDENT LIFE
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'UW Tacoma Campus Tours'"
             href="http://www.tacoma.uw.edu/admissions/visit"
          >
            Plan your visit: Tacoma campus tours
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'UW Tacoma Student Housing'"
             href="https://www.tacoma.uw.edu/housing"
          >
            Student housing
          </a>
        </li>
        <li class="mb-1">
          <a
            v-out="'UW Tacoma New Student programs'"
            href="https://www.tacoma.uw.edu/new-students"
          >
            New Student Programs
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'UW Tacoma Disability Resources for Students (DRS)'"
             href="http://www.tacoma.uw.edu/drsuwt"
          >
            Disability Resources for Students (DRS)
          </a>
        </li>
      </ul>
      <h3 class="h6 myuw-font-encode-sans">
        Next steps if you are admitted
      </h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'Next Steps for Admitted UW Tacoma Students'"
             href="https://www.tacoma.uw.edu/registrar/newly-admitted-students"
          >
            Accept your admission offer and pay the fee
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'New UW Tacoma Student Orientation'"
             href="https://www.tacoma.uw.edu/new-students"
          >
            Sign up for New Student Orientation
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'Next Steps for Admitted UW Tacoma Students'"
             href="https://www.tacoma.uw.edu/admissions/i-was-admitted"
          >
            See additional steps required to enroll at UW Tacoma
          </a>
        </li>
        <li v-if="applicantData.is_international">
          <a v-out="'UW Tacoma Intl student to-do list'"
             href="http://www.tacoma.uw.edu/iss/to-do-list"
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
import LinkButton from '../../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link-button': LinkButton,
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
