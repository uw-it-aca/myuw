<template>
  <div class="myuw-text-md">
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">
      Instructors
    </h3>
    <div>
      <ol class="list-unstyled myuw-text-md mb-0">
        <li v-for="(instructor, i) in instructors" :key="i" class="mb-2">
          <strong>{{ instructor.display_name }}</strong>
          <div v-if="instructorPrimaryTitle(instructor)"
               class="text-muted font-italic"
          >
            {{ instructorPrimaryTitle(instructor) }}
          </div>
          <div v-if="!hasContactDetails(instructor)" class="text-muted">
            No contact information available for this instructor.
          </div>
          <div v-else>
            <a
              v-for="(email, j) in instructor.email_addresses"
              :key="`email-${j}`"
              v-inner="'Email instructor'"
              :href="`mailto:${email}`"
              class="d-block"
            >
              {{ email }}
            </a>
            <a
              v-for="(phone, j) in instructor.phones"
              :key="`phone-${j}`"
              v-inner="'Tel instructor'"
              :href="`tel:${formatPhoneNumberLink(phone)}`"
              class="d-block"
            >
              {{ formatPhoneNumberDisaply(phone) }}
            </a>
            <div
              v-for="(address, j) in instructor.addresses"
              :key="`address-${j}`"
            >
              {{ address }}
            </div>
          </div>
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    instructors: {
      type: Array,
      required: true,
    },
  },
  methods: {
    hasContactDetails(instructor) {
      return (
        instructor.email_addresses.length > 0 ||
        instructor.phones.length > 0 ||
        instructor.addresses.length > 0
      );
    },
    instructorPrimaryTitle(instructor) {
      const titles = instructor.positions
          .filter((p) => p.is_primary)
          .map((p) => p.title);
      return titles.length > 0 ? titles[0] : null;
    },
  },
};
</script>
