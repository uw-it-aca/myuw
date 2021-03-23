<template>
  <uw-card :loaded="true">
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        UW Resources
      </h3>
    </template>
    <template #card-body>
      <p class="myuw-text-md">Explore tools, services, and resources by popular topics.</p>
      
      <ul class="list-unstyled myuw-text-lg myuw-resource-links">
        <b-container fluid>
          <b-row>
            <b-col md="6">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ml-1" href="/resources/#academics">Academic Resources</a>
              </li>
            </b-col>
            <b-col md="6">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ml-1" href="/resources/#studentfinances">Student Finances</a>
              </li>
            </b-col>
          </b-row>
          <b-row>
            <b-col md="6">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ml-1"
                   href="/resources/#accountsidentityandemail"
                >Accounts, Identity, and Email</a>
              </li>
            </b-col>
            <b-col md="6">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ml-1" href="/resources/#employment">Employment</a>
              </li>
            </b-col>
          </b-row>
        </b-container>
      </ul>
      <hr>
      <div>
        <h4 class="h6 mb-3 text-dark-beige myuw-font-encode-sans">
          More topics
        </h4>
        <ul class="list-inline myuw-text-md">
          <li class="list-inline-item">
            <a href="/resources/#teaching">Teaching</a>
          </li>
          <li class="list-inline-item">
            <a href="/resources/#libraries">Libraries</a>
          </li>
          <li class="list-inline-item">
            <a href="/resources/#campuslife">Campus Life</a>
          </li>
          <li class="list-inline-item">
            <a href="/resources/#eventsactivities">Events and Activities</a>
          </li>
          <li class="list-inline-item">
            <a href="/resources/#servicesforfacultyandstaff">Services for Faculty and Staff</a>
          </li>
        </ul>
      </div>
    </template>
  </uw-card>
</template>

<script>
import {
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data() {
    return {
      faChevronRight,
    };
  },
};
</script>
<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

.myuw-resource-links {
  a {
    color: black;
  }
  svg {
    color: $link-color;
  }

}

</style>
