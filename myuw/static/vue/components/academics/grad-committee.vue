<template>
  <uw-card
    v-if="showCard"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Committees
      </h2>
    </template>
    <template #card-body>
      <div>
        <ul class="list-unstyled myuw-text-md">
          <li v-for="(committee, index) in committees" :key="index"
              class="mb-4"
          >
            <h3 class="h6 text-dark-beige myuw-font-encode-sans">
              {{ committee.committee_type }}
            </h3>
            <ol class="list-unstyled">
              <li v-for="(member, mindex) in committee.members" :key="mindex"
                  class="mb-3"
              >
                <div v-text="formatMemberString(member)" />
                <div v-if="member.dept">
                  {{ member.dept }}
                </div>
                <div v-if="member.email">
                  <a :href="`mailto:${member.email}`">
                    {{ member.email }}
                  </a>
                </div>
              </li>
            </ol>
          </li>
        </ul>
      </div>
      <div class="text-end">
        <uw-link-button
          href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/">
          Go to MyGrad
        </uw-link-button>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your committees request information
      right now. In the meantime, try the
      <a v-out="'MyGrad'"
        href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/"
      >MyGrad Program</a> page.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link-button': LinkButton
  },
  computed: {
    ...mapState({
      isGrad: (state) => state.user.affiliations.grad,
      committees: (state) => state.grad.value.committees,
    }),
    ...mapGetters('grad', [
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showError: function() {
      return this.statusCode !== 404;
    },
    showCard: function() {
      return !this.isReady || (this.isGrad && (this.committees != undefined));
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    formatMemberString(member) {
      let memberString = member.first_name + ' ' + member.last_name;
      if (member.member_type) {
        memberString = memberString.concat(', ', member.member_type);
      }
      if (member.reading_type) {
        memberString = memberString.concat(', ', member.reading_type);
      }
      return memberString;
    },
    ...mapActions('grad', ['fetch']),
  },
};
</script>
