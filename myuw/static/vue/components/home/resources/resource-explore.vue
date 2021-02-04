<template>
  <uw-card :loaded="true">
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        UW Resources
      </h3>
    </template>
    <template #card-body>
      <p>Explore tools, services, and resources by popular topics.</p>
      
      <ul>
        <li>
          <font-awesome-icon :icon="['fa', 'chevron-right']"/>
          <a href="/resources/#academics">Academic Resources</a>
        </li>
        <li>
          <font-awesome-icon :icon="['fa', 'chevron-right']"/>
          <a href="/resources/#accountsidentityandemail">Accounts, Identity, and Email</a>
        </li>
        <li>
          <font-awesome-icon :icon="['fa', 'chevron-right']"/>
          <a href="/resources/#studentfinances">Student Finances</a>
        </li>
        <li>
          <font-awesome-icon :icon="['fa', 'chevron-right']"/>
          <a href="/resources/#employment">Employment</a>
        </li>
      </ul>

      <div>
          <h4>
            More topics
          </h4>
          <ul class="myuw-inline-list">
            <li>
              <a href="/resources/#teaching">Teaching</a>
            </li>
            <li>
              <a href="/resources/#libraries">Libraries</a>
            </li>
            <li>
              <a href="/resources/#campuslife">Campus Life</a>
            </li>
            <li>
              <a href="/resources/#eventsactivities">Events and Activities</a>
            </li>
            <li>
              <a href="/resources/#servicesforfacultyandstaff">Services for Faculty and Staff</a>
            </li>
          </ul>
      </div>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
};
</script>
