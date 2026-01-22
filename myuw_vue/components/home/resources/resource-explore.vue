<template>
  <uw-card :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        UW Resources
      </h2>
    </template>
    <template #card-body>
      <p class="myuw-text-md">Explore tools, services, and resources by popular topics.</p>

      <div class="myuw-text-lg myuw-resource-links">
        <div class="container">
          <div class="row">
            <ul class="col-md-6 list-unstyled m-0">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ms-1" href="/resources/#academics">Academic Resources</a>
              </li>
            </ul>
            <ul class="col-md-6 list-unstyled m-0">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ms-1" href="/resources/#studentfinances">Student Finances</a>
              </li>
            </ul>
          </div>
          <div class="row">
            <ul class="col-md-6 list-unstyled m-0">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ms-1"
                   href="/resources/#emailandaccountsandidentity"
                >Accounts, Identity, and Email</a>
              </li>
            </ul>
            <ul class="col-md-6 list-unstyled m-0">
              <li class="mb-2">
                <font-awesome-icon :icon="faChevronRight" aria-hidden="true"/>
                <a class="ms-1" href="/resources/#employment">Employment</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <hr class="bg-secondary">
      <div>
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          More topics
        </h3>
        <ul class="list-inline myuw-text-md mb-1">
          <li class="list-inline-item">
            <a href="/resources/#research">Research</a>
          </li>
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
            <a href="/resources/#eventsandactivities">Events and Activities</a>
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
@import '../../../../myuw/static/css/myuw/variables.scss';

.myuw-resource-links {
  a {
    color: black;
  }
  svg {
    color: $link-color;
  }

}

</style>
