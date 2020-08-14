<template>
    <uw-card :loaded="isReady">
        <template #card-heading>
            <h3>Notices</h3>
        </template>
        <template #card-body v-if="!isErrored">
            <p v-if="notices.length == 0">
                You do not have any notices at this time.
            </p>
            <ul class="list-unstyled" v-else>
                <li v-for="notice in notices" :key="notice.id_hash">
                    <div>
                         <span>
                            <span class="font-weight-bold text-danger" v-if="notice.is_critical">
                                Critical:
                            </span>
                            <b-link v-b-toggle="notice.id_hash"
                                class="p-0" variant="link"
                                v-html="notice.notice_title">
                            </b-link>
                            <b-badge v-if="!notice.is_read" variant="warning" class="font-weight-normal">New</b-badge>
                        </span>
                    </div>
                    <b-collapse @show="onShowNotice(notice)"
                                :id="notice.id_hash" tabindex="0">
                        <div v-html="notice.notice_body"></div>
                    </b-collapse>
                </li>
            </ul>
        </template>
        <template #card-body v-else>
            <p class="text-danger">
                <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>
                An error occurred and MyUW cannot load your notices right now. Please try again later.
            </p>
        </template>
    </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {};
  },
  computed: {
    ...mapState({
      notices: (state) => {
        return state.notices.value.filter(
            (notice) => notice.is_critical ||
              notice.category.includes('Legal') ||
              notice.location_tags.includes('notices_date_sort') ||
              notice.location_tags.includes('notice_banner'),
        ).sort((n1, n2) => {
          if (n1.is_critical !== n2.is_critical) return n2.is_critical;
          return n2.date - n1.date;
        });
      },
    }),
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    onShowNotice(notice) {
      if (!notice.is_read) {
        this.setRead(notice);
      }
    },
    ...mapActions('notices', [
      'fetch',
      'setRead',
    ]),
  },
};
</script>

<style lang="scss" scoped>

</style>
