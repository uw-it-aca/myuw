<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h2>
    </template>
    <template v-else #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Seattle Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h2>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h3 class="h6 myuw-font-encode-sans">Application status</h3>
      <p class="myuw-text-md">
        For application status, contact the Office of the University Registrar:
      </p>
      <div class="container mb-3 myuw-text-md">
        <div class="row">
          <div class="col">Email</div>
          <div class="col">
            <a v-out="'Contact Registrar Office'" href="mailto:regoff@uw.edu">regoff@uw.edu</a>
          </div>
        </div>
        <div class="row">
          <div class="col">Phone</div>
          <div class="col">(206) 543-4000</div>
        </div>
        <div class="row">
          <div class="col">Location</div>
          <div class="col">225 Schmitz Hall</div>
        </div>
      </div>

      <h3 class="h6 myuw-font-encode-sans">Registration for returning student</h3>
      <p>
        You must
        <a href="https://sdb.admin.uw.edu/enroll/uwnetid/">confirm your enrollment</a>
        and pay the enrollment fee prior to being able to register.
      </p>
      <p>
        You will then register beginning with Registration Period II for your returning quarter.
        Check dates on the
        <a href="http://www.washington.edu/students/reg/calendar.html">Academic Calendar</a>.
      </p>

      <h3 class="h6 myuw-font-encode-sans">Resources for Seattle applicants</h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'Student Financial Aid'" href="https://www.washington.edu/financialaid/">
            Student financial aid, loans, and scholarships
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'Student Guide'" href="http://www.washington.edu/students/">
            Check out the Student Guide
          </a>
        </li>
        <li class="mb-1">
          <a href="http://www.washington.edu/students/reg/calendar.html">
            View the UW Academic Calendar
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <uw-link-button class="my-4" href="https://sdb.admin.uw.edu/admissions/uwnetid/appstatus.asp">
        View your {{ applicantData.type }} application status
      </uw-link-button>

      <h3 class="h6 myuw-font-encode-sans">Resources for Seattle applicants</h3>
      <h4 class="h6">ADMISSIONS</h4>
      <ul class="list-unstyled myuw-text-md">
        <li v-if="applicantData.is_freshman" class="mb-1">
          <a href="https://admit.washington.edu/apply/dates-deadlines/">
            Key dates &amp; deadlines for freshmen
          </a>
        </li>
        <li v-if="applicantData.is_transfer" class="mb-1">
          <a href="https://admit.washington.edu/apply/dates-deadlines/#transfer">
            Key dates &amp; deadlines for transfer students
          </a>
        </li>
        <li v-if="applicantData.if_post_bac" class="mb-1">
          <a href="https://admit.washington.edu/apply/dates-deadlines/#postbac">
            Key dates &amp; deadlines for postbaccalaureates
          </a>
        </li>
      </ul>

      <h4 class="h6">FINANCES</h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a href="https://www.washington.edu/financialaid/">
            Student financial aid, loans, and scholarships
          </a>
        </li>
        <li class="mb-1">
          <a
            href="https://www.washington.edu/financialaid/applying-for-aid/key-dates-and-deadlines/"
          >
            Financial aid key dates and deadlines
          </a>
        </li>
        <li class="mb-1">
          <a href="https://admit.washington.edu/costs/coa/">
            Understand total cost of attendance
          </a>
        </li>
      </ul>

      <h4 class="h6">STUDENT LIFE</h4>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a href="http://admit.washington.edu/Visit"> Plan your visit: Seattle campus tours </a>
        </li>
        <li class="mb-1">
          <a href="https://hfs.uw.edu/Live"> Explore campus living </a>
        </li>
        <li class="mb-1">
          <a href="http://depts.washington.edu/uwdrs/"> Disability Resources for Students (DRS) </a>
        </li>
      </ul>
      <h3 class="h6 myuw-font-encode-sans">Next steps if you are admitted</h3>
      <ul style="list-style-type: circle" class="myuw-text-md">
        <li class="mb-1">
          <a
            v-out="'Accept admission offer'"
            href="https://www.washington.edu/newhuskies/must-do/accept/"
          >
            Accept your admission offer and pay the fee
          </a>
        </li>
        <li class="mb-1">
          <a href="http://fyp.washington.edu/getting-started-at-the-university-of-washington/">
            Register for an Advising &amp; Orientation session
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/newhuskies/must-do/send-proof-of-immunity/">
            Make sure you’re immunized
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/newhuskies/must-do/#photo">
            Submit a photo for your Husky Card
          </a>
        </li>
        <li class="mb-1">
          <a href="http://www.washington.edu/newhuskies/must-do/">
            See additional steps required to enroll at the UW
          </a>
        </li>
        <li v-if="applicantData.is_international" class="mb-1">
          <a v-out="'Intl student checklist'" href="https://iss.washington.edu/new-students/">
            International students: additional steps
          </a>
        </li>
      </ul>
      <h3 class="h6 myuw-font-encode-sans">Additional resources for admitted students</h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a
            href="http://www.washington.edu/uaa/advising/academic-planning/majors-and-minors/list-of-undergraduate-majors/"
          >
            View undergraduate majors
          </a>
        </li>
        <li class="mb-1">
          <a href="http://fyp.washington.edu/"> Learn about First Year Programs </a>
        </li>
        <li class="mb-1">
          <a href="http://www.washington.edu/students/"> Check out the Student Guide </a>
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
