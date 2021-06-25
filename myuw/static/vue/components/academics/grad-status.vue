<template>
  <uw-card
    v-if="showCard"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Graduate Request Status
      </h2>
    </template>
    <template #card-body>
      <div v-if="petitions">
        <div id="petition-reqs">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Petition Requests
          </h3>
          <ul v-for="(petition, index) in petitions" :key="index"
              class="list-unstyled myuw-text-md"
          >
            <li class="mb-3">
              <h5 class="h6 mb-0">
                {{ petition.description }}
              </h5>
              <div v-if="petition.dept_recommend"
                   class="d-flex myuw-font-encode-sans"
              >
                <div class="flex-fill w-50">
                  Department Recommendation
                </div>
                <div class="flex-fill w-50 text-right">
                  {{ petition.dept_recommend }}
                </div>
              </div>
              <div v-if="petition.gradschool_decision"
                   class="d-flex myuw-font-encode-sans"
              >
                <div class="flex-fill w-50">
                  Graduate School Decision
                </div>
                <div class="flex-fill w-50 text-right">
                  {{ petition.gradschool_decision }}
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="leaves">
        <div id="leave-reqs">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Leave Requests
          </h3>
          <ul v-for="(leave, index) in leaves" :key="index"
              class="list-unstyled myuw-text-md"
          >
            <li class="mb-1">
              <h5 class="h6 mb-0">
                <template v-for="(term, termIndex) in leave.terms">
                  <span v-if="termIndex > 0" :key="termIndex">, </span>
                  {{ term.quarter + " " + term.year }}
                </template> Leave
              </h5>
              <div class="d-flex myuw-font-encode-sans">
                <div class="flex-fill w-50">
                  Status
                </div>
                <div class="flex-fill w-50 text-right">
                  <span v-if="leave.status === 'Approved'">
                    Approved<br>
                    <a
                      v-out="'MyGrad Payment Portal'"
                      href="https://webapps.grad.uw.edu/mgp-stu/uwnetid/default.aspx"
                      class="font-weight-normal"
                    >Pay Your Fee To Confirm</a>
                  </span>
                  <span v-else>
                    {{ leave.status }}
                  </span>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="degrees">
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          Degree and Exam Requests
        </h3>
        <ul v-for="(degree, index) in degrees" :key="index"
            class="list-unstyled myuw-text-md"
        >
          <li class="mb-1">
            <h5 class="h6 mb-0">
              {{ degree.req_type }}, {{ degree.target_award_quarter }}
              {{ degree.target_award_year }}
            </h5>
            <div>
              {{ degree.degree_title }}
            </div>
            <div class="d-flex myuw-font-encode-sans">
              <div class="flex-fill w-50">
                Status
              </div>
              <div class="flex-fill w-50 text-right">
                {{ degree.status }}
              </div>
            </div>
          </li>
        </ul>
      </div>

      <div class="text-right">
        <uw-link-button
          href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/">
          Go to MyGrad
        </uw-link-button>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your graduate request information
      right now. In the meantime, try the
      <a
        v-out="'MyGrad'"
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
    'uw-link-button': LinkButton,
  },
  computed: {
    ...mapState({
      petitions: (state) => {
        const petitionList = state.grad.value.petitions;
        if (petitionList) {
          petitionList.forEach((petition) => {
            if (petition.dept_recommend === 'Pending' ||
                petition.dept_recommend === 'Withdraw') {
              petition.gradschool_decision = null;
            }
            if (petition.gradschool_decision === 'Approved') {
              petition.dept_recommend = null;
            }
          });
        }
        return petitionList;
      },
      leaves: (state) => state.grad.value.leaves,
      degrees: (state) => state.grad.value.degrees,
      isGrad: (state) => state.user.affiliations.grad,
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
      return !this.isReady || this.isGrad &&
              (this.leaves || this.petitions || this.degrees);
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('grad', ['fetch']),
  },
};
</script>
