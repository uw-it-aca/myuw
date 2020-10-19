<template>
  <uw-card
    v-if="showCard"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">
        Graduate Request Status
      </h3>
    </template>
    <template #card-body>
      <div>
        <ul>
          <li v-for="(committee, index) in committees" :key="index">
            <h4>
              {{ committee.committee_type }}
            </h4>
            <ol>
              <li v-for="(member, mindex) in committee.members" :key="mindex">
                <span v-text="formatMemberString(member)" />
                <br>
                <span v-if="member.dept">{{ member.dept }}</span>
                <br>
                <span v-if="member.email">
                  <a :href="`mailto:${member.email}`">
                    {{ member.email }}
                  </a>
                </span>
              </li>
            </ol>
          </li>
        </ul>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your committees request information
      right now. In the meantime, try the
      <a
        href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/"
        data-linklabel="MyGrad"
        target="_blank"
      >MyGrad program page</a>.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
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
      console.log(memberString);
      return memberString;
    },
    ...mapActions('grad', ['fetch']),
  },
};
</script>
