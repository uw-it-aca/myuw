<template>
  <b-form-group label="Request a single email list for:">
    <b-form-radio-group
      id="`joint-section_joint_${emailList.section_id}`"
      v-model="sectionJointList">
      <b-form-radio value="joint" checked>
        {{emailList.course_abbr}}
        {{emailList.course_number}}
        {{emailList.section_id}}
        <span v-for="(section, i) in emailList.joint_sections" :key="i">
          +
          {{section.course_abbr}}
          {{section.course_number}}
          {{section.section_id}}
        </span>
        <p class="text-muted">
          Mailing list address:
          {{emailList.joint_section_list.list_address}}@uw.edu
        </p>
      </b-form-radio>
      <b-form-radio value="single">
        {{emailList.course_abbr}}
        {{emailList.course_number}}
        {{emailList.section_id}}
        <p class="text-muted">
          Mailing list address:
          {{emailList.section_list.list_address}}@uw.edu
        </p>
      </b-form-radio>
    </b-form-radio-group>
  </b-form-group>
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
  watch: {
    sectionJointList(newVal) {
      this.$emit('selected', this.generateFormData(newVal, this.emailList.section_list));
    }
  },
  mounted() {
    this.$emit(
      'selected',
      this.generateFormData(this.sectionJointList, this.emailList.section_list)
    );
  },
  methods: {
    generateFormData(listType, sectionList) {
      return {
        section_joint_list: listType,
        [`section_id_${sectionList.section_id}`]: sectionList.section_label,
      };
    },
  },
}
</script>