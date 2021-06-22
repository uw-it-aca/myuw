<template>
  <div>
    <p>
      <strong>
        Request a single email list for
        {{emailList.course_abbr}}
        {{emailList.course_number}}
        {{emailList.section_id}},
        {{titleCaseWord(emailList.quarter)}}
        {{emailList.year}}.
      </strong>
      <span v-if="!emailList.no_secondary_section && !emailList.has_lists">
        <br/>
        <span>
          Need more email lists for this class?
          <b-link @click="$emit('reqmulti')">
            Request multiple email lists.
          </b-link>
        </span>
      </span>
    </p>

    <ul>
      <li class="mb-1">
        Mailing list address:
        {{emailList.section_list.list_address}}@uw.edu
      </li>
      <li class="mb-1">Mailing list will stay synced with the official class list</li>
    </ul>
  </div>
</template>

<script>
export default {
  model: {
    prop: 'formData',
    event: 'selected'
  },
  props: {
    emailList: {
      type: Object,
      required: true,
    },
    formData: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      sectionJointList: 'joint',
    };
  },
  mounted() {
    const sectionList = this.emailList.section_list;
    this.$emit('selected', {
      [`section_single_${sectionList.section_id}`]: sectionList.section_label,
    });
  },
}
</script>