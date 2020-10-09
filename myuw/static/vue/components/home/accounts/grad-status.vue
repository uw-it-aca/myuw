<template>
  <uw-card
    v-if="!isReady || is_grad"
    :loaded="isReady" :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">
        Graduate Request Status
      </h3>
    </template>
    <template #card-body>
      <div v-if="petitions.length > 0">
        <div class="card-badge-container" id="petition-reqs">
          <h4>Petition Requests</h4>

          <ul v-for="(petition, index) in petitions" :key="index" class="card_list">
            <li>
              <div class="card-badge clearfix">
                <h5>{{ petition.description }}</h5>
                <ul class="recommendation-list">
                  <li v-if="petition.dept_recommend" class="clearfix">
                    <div class="pull-left">
                      <span class="card-badge-label">Department Recommendation</span>
                    </div>
                    <span>
                      <span class="card-badge-value">{{ petition.dept_recommend }}</span>
                    </span>
                  </li>

                  <li v-if="petition.gradschool_decision" class="clearfix">
                    <div class="pull-left">
                      <span class="card-badge-label">Graduate School Decision</span>
                    </div>
                    <span>
                      <span class="card-badge-value">{{ petition.gradschool_decision }}</span>
                    </span>
                  </li>
                </ul>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="leaves.length > 0">
        <div class="card-badge-container" id="leave-reqs">
          <h4>Leave Requests</h4>

          <ul v-for="(leave, index) in leaves" :key="index" class="card_list">
            <li>
              <div class="card-badge clearfix">
                <h5>
                  <template v-for="(term, termIndex) in leave.terms">
                    <span :key="termIndex">
                      <span v-if="termIndex > 0">
                        , 
                      </span>
                      {{ term.quarter + ' ' + term.year }} Leave
                  </template>
                </h5>
                <div class="pull-left">
                  <span class="card-badge-label">Status</span>
                </div>
                <span>
                  <span class="card-badge-value">
                  </span>
                </span>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="degrees.length > 0">

      </div>
        
      <div class="clearfix">
        <div class="card-badge-action pull-right">
          <a href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/" data-linklabel="MyGrad" target="_blank">Go to MyGrad</a>
        </div>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your graduate request information right now.
      In the meantime, try the
      <a href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/" data-linklabel="MyGrad" target="_blank">MyGrad program page</a>.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      petitions: (state) => {
        const petitionList = state.grad.value.petitions;
        petitionList.forEach((petition) => {
          if (petition.dept_recommend === "Pending" ||
              petition.dept_recommend === "Withdraw") {

            petition.gradschool_decision = null;
          }
          if (petition.gradschool_decision === "Approved") {
            petition.dept_recommend = null;
          }
        });
        return petitionList;
      },
      leaves: (state) => state.grad.value.leaves,
      degrees: (state) => state.grad.value.degrees,
      is_grad: (state) => state.user.affiliations.grad,
    }),
    ...mapGetters('grad', [
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showError: function() {
      return this.statusCode !== 404;
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
