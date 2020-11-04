<template>
  <div>
    <!-- creates line spacer above instructor info -->
    <div v-if="showRowHeading" class="d-flex">
      <div class="w-25">
        &nbsp;
      </div>
      <div class="flex-fill">
        <hr>
      </div>
    </div>
    <!-- begin instructor info display -->
    <div :class="[!showRowHeading ? 'flex-column' : '']" class="d-flex">
      <h5
        class="w-25 font-weight-bold myuw-text-md"
      >
        Instructors
      </h5>
      <div class="flex-fill">
        <ol class="list-unstyled myuw-text-md mb-0">
          <li v-for="(instructor, i) in instructors" :key="i" class="mb-2">
            <strong>{{ instructor.display_name }}</strong>
            <div v-if="instructorPrimaryTitle(instructor)" class="text-muted">
              {{ instructorPrimaryTitle(instructor) }}
            </div>
            <div v-if="!hasContactDetails(instructor)" class="text-muted">
              No contact information available for this instructor.
            </div>
            <div v-else>
              <a
                v-for="(email, j) in instructor.email_addresses"
                :key="`email-${j}`" :href="`mailto:${email}`"
                class="d-block"
              >
                {{ email }}
              </a>
              <a
                v-for="(phone, j) in instructor.phones"
                :key="`phone-${j}`"
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
  </div>
</template>

<script>
export default {
  props: {
    instructors: {
      type: Array,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
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
