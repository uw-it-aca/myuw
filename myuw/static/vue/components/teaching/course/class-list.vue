<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Enrollment
    </h5>
    <div class="mb-0 w-100 myuw-text-md">
        <uw-enrollment :section="section" />
        <span>
        <b-link v-if="isDownloadPossible"
          id="csv_download_class_list"
          @click="downloadCL"
        >
          <font-awesome-icon :icon="faDownload" /> Download (CSV)
        </b-link>
        </span>
      </div>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import {
  faDownload,
} from '@fortawesome/free-solid-svg-icons';
import Enrollment from '../../_common/course/inst/enrollment.vue';

export default {
  components: {
    'uw-enrollment': Enrollment,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeader: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      faDownload,
    };
  },
  computed: {
    ...mapState('classlist', {
      allData: (state) => state.value,
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
    }),
    getKey() {
      return this.section.apiTag.replace(/&amp;/g, '%26');
    },
    isDownloadPossible() {
      return this.isReadyTagged(this.getKey);
    },
    sectionDetail() {
      return this.allData[this.getKey];
    },
  },
  created() {
    this.fetchClasslist(this.getKey);
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
    downloadCL() {
      this.downloadClassList(this.sectionDetail);
    },
  }
};
</script>
