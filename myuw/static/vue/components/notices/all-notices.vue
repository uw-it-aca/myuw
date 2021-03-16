<template>
  <div v-if="isReady">
    <div class="d-flex border-bottom pb-3">
      <div class="ml-auto myuw-text-md">
        <b-link
          v-if="!everyNoticeListExpanded"
          v-out="'Expand All Notices'"
          title="Show all notice information"
          @click="expandAll()"
        >
          Expand All
        </b-link>
        <b-link v-else
          v-out="'Hide All Notices'"
          title="Hide all notice information"
          @click="collapseAll()"
        >
          Collapse All
        </b-link>
      </div>
    </div>
    <div v-if="hasAnyNotices">
      <notice-list
        v-for="(noticeList, i) in noticeGroups"
        ref="notice_list"
        :key="i"
        :title="noticeList[0]"
        :notices="noticeList[1]"
        :critical="noticeList[2]"
      />
    </div>
    <uw-card v-else loaded>
      <template #card-heading>
        No Notices Found
      </template>
      <template #card-body>
        You don&rsquo;t appear to have any notices to display at the moment.
      </template>
    </uw-card>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import {mapGetters, mapState, mapActions} from 'vuex';

import Card from '../_templates/card.vue';
import NoticeList from './notice-list.vue';
dayjs.extend(require('dayjs/plugin/isToday'));
dayjs.extend(require('dayjs/plugin/weekOfYear'));

export default {
  components: {
    'uw-card': Card,
    'notice-list': NoticeList,
  },
  data() {
    return {
      isDeepMounted: false,
    };
  },
  computed: {
    ...mapState('notices', {
      allNotices: (state) => state.value,
    }),
    ...mapGetters('notices', ['isReady']),
    criticalNotices() {
      const finaidCriticalTags = [
        "tuition_aidhold",
        "tuition_missingdocs",
        "tuition_loanpromissory",
        "tuition_loancounseling",
        "tuition_acceptreject",
        "tuition_disbursedateA",
        "tuition_disbursedateB",
        "tuition_direct_deposit",
        "tuition_aid_prioritydate",
      ];

      return this.allNotices.filter((n) => {
        return n.is_critical && (
          n.sws_category !== "StudentFinAid" ||
          finaidCriticalTags.some((ft) => n.location_tags.includes(ft))
        )
      });
    },
    legalNotices() {
      return this.allNotices.filter((n) => n.category === "Legal");
    },
    timedNotices() {
      const notices = {
        today: [],
        thisWeek: [],
        nextWeek: [],
        future: [],
      };
      const today = this.nowDatetime();
      this.allNotices
        .filter((n) => n.location_tags.includes('notices_date_sort'))
        .forEach((n) => {
          if (!n.date) {
            notices.future.push(n);
          } else if (n.date.isToday()) {
            notices.today.push(n);
          } else if (n.date.week() === today.week()) {
            notices.thisWeek.push(n);
          } else if (n.date.week() === today.week() + 1) {
            notices.nextWeek.push(n);
          } else if (n.date > today) {
            notices.future.push(n);
          }
        });
      
      return notices;
    },
    hasAnyNotices() {
      return this.criticalNotices.length !== 0 ||
             this.legalNotices.length !== 0 ||
             this.timedNotices.today.length !== 0 ||
             this.timedNotices.thisWeek.length !== 0 ||
             this.timedNotices.nextWeek.length !== 0 ||
             this.timedNotices.future.length !== 0;
    },
    noticeGroups() {
      return [
        [`${this.criticalNotices.length} Critical`, this.criticalNotices, true],
        ["Today", this.timedNotices.today, false],
        ["This week", this.timedNotices.thisWeek, false],
        ["Next week", this.timedNotices.nextWeek, false],
        ["Upcoming weeks", this.timedNotices.future, false],
        ["Legal", this.legalNotices, false],
      ]
    },
    everyNoticeListExpanded() {
      if (this.isDeepMounted) {
        return this.$refs.notice_list &&
              this.$refs.notice_list.every((n) => {
                if (n.$refs.collapsible) {
                  return n.$refs.collapsible.show;
                }
                return true;
              });
      }
      return true;
    },
  },
  created() {
    this.fetch();
  },
  updated() {
    if (!this.isDeepMounted) {
      this.isDeepMounted = true;
    }
  },
  methods: {
    ...mapActions('notices', ['fetch']),
    expandAll() {
      this.$refs.notice_list.forEach((n) => {
        if (n.$refs.collapsible) {
          n.$refs.collapsible.show = true;
        }
      });
    },
    collapseAll() {
      this.$refs.notice_list.forEach((n) => {
        if (n.$refs.collapsible) {
          n.$refs.collapsible.show = false;
        }
      });
    },
  },
}
</script>