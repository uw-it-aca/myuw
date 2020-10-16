<template>
  <uw-card
    v-if="showCard"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="text-dark-beige">Graduate Request Status</h3>
    </template>
    <template #card-body>
      <div v-if="petitions">
        <div id="petition-reqs">
          <h4>Petition Requests</h4>

          <ul v-for="(petition, index) in petitions" :key="index">
            <li>
              <h5>{{ petition.description }}</h5>
              <ul>
                <li v-if="petition.dept_recommend">
                  <div>
                    <span> Department Recommendation </span>
                  </div>
                  <span>
                    <span>
                      {{ petition.dept_recommend }}
                    </span>
                  </span>
                </li>

                <li v-if="petition.gradschool_decision">
                  <div>
                    <span> Graduate School Decision </span>
                  </div>
                  <span>
                    {{ petition.gradschool_decision }}
                  </span>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="leaves">
        <div id="leave-reqs">
          <h4>Leave Requests</h4>

          <ul v-for="(leave, index) in leaves" :key="index">
            <li>
              <h5>
                <template v-for="(term, termIndex) in leave.terms"
                  ><span :key="termIndex" v-if="termIndex > 0">, </span
                  >{{ term.quarter + " " + term.year }}</template
                >
                Leave
              </h5>
              <div>Status</div>
              <span v-if="leave.status === 'Approved'">
                Approved<br />
                <a
                  target="_blank"
                  href="https://apps.grad.uw.edu/mgp-stu/uwnetid/default.aspx"
                  data-linklabel="MyGrad Payment Portal"
                  >Pay Your Fee To Confirm</a
                >
              </span>
              <span v-else>
                {{ leave.status }}
              </span>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="degrees">
        <h4>Degree and Exam Requests</h4>
        <ul v-for="(degree, index) in degrees" :key="index">
          <li>
            <h5>
              {{ degree.req_type }}, {{ degree.target_award_quarter }}
              {{ degree.target_award_year }}
            </h5>
            <div>
              {{ degree.degree_title }}
            </div>
            <div>
              <span>Status</span>
            </div>
            <span>{{ degree.status }}</span>
          </li>
        </ul>
      </div>

      <div>
        <a
          href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/"
          data-linklabel="MyGrad"
          target="_blank"
          >Go to MyGrad</a
        >
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your graduate request information
      right now. In the meantime, try the
      <a
        href="https://grad.uw.edu/for-students-and-post-docs/mygrad-program/"
        data-linklabel="MyGrad"
        target="_blank"
        >MyGrad program page</a
      >.
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from "vuex";
import Card from "../_templates/card.vue";

export default {
  components: {
    "uw-card": Card,
  },
  computed: {
    ...mapState({
      petitions: (state) => {
        const petitionList = state.grad.value.petitions;
        if (petitionList) {
          petitionList.forEach((petition) => {
            if (
              petition.dept_recommend === "Pending" ||
              petition.dept_recommend === "Withdraw"
            ) {
              petition.gradschool_decision = null;
            }
            if (petition.gradschool_decision === "Approved") {
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
    ...mapGetters("grad", ["isReady", "isErrored", "statusCode"]),
    showError: function () {
      return this.statusCode !== 404;
    },
    showCard: function () {
      return !this.isReady || this.isGrad && (this.leaves || this.petitions || this.degrees);
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions("grad", ["fetch"]),
  },
};
</script>
