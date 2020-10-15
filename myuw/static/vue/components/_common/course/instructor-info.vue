<template>
  <div>
    <h5>Instructors</h5>
    <ol>
      <li v-for="(instructor, i) in instructors" :key="i">
        <strong>{{instructor.display_name}}</strong>
        <span v-if="instructorPrimaryTitle(instructor)">
          {{instructorPrimaryTitle(instructor)}}
        </span>
        <span v-if="!hasContactDetails(instructor)">
          No contact information available for this instructor.
        </span>
        <div v-else>
          <a
            v-for="(email, i) in instructor.email_addresses"
            :key="`email-${i}`" :href="`mailto:${email}`"
          >
            {{email}}
          </a>
          <a
            v-for="(phone, i) in instructor.phones"
            :key="`phone-${i}`" :href="`tel:${formatPhoneNumberLink(phone)}`"
          >
            {{formatPhoneNumberDisaply(phone)}}
          </a>
          <span
            v-for="(address, i) in instructor.addresses"
            :key="`address-${i}`"
          >
            {{address}}
          </span>
        </div>
      </li>
    </ol>
  </div>
</template>

<script>
export default {
  props: {
    instructors: {
      type: Array,
      required: true,
    }
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
      let titles = instructor.positions
        .filter((p) => p.is_primary)
        .map((p) => p.title);
      return titles.length > 0 ? titles[0] : null;
    }
  }
}
</script>