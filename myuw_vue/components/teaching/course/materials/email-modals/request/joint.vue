<template>
  <fieldset class="form-group">
    <legend>
      Request a single email list for:
    </legend>
    <div class="form-check">
      <input
        id="joint_radio"
        v-model="sectionJointList"
        class="form-check-input"
        type="radio"
        value="joint"
        checked
      >
      <label class="form-check-label" for="joint_radio">
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
      </label>
    </div>
    <div class="form-check">
      <input
        id="single_radio"
        v-model="sectionJointList"
        class="form-check-input"
        type="radio"
        value="single"
        checked
      >
      <label class="form-check-label" for="single_radio">
        {{emailList.course_abbr}}
        {{emailList.course_number}}
        {{emailList.section_id}}
        <p class="text-muted">
          Mailing list address:
          {{emailList.section_list.list_address}}@uw.edu
        </p>
      </label>
    </div>
  </fieldset>
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
      this.$emit('selected', this.generateFormData(newVal));
    }
  },
  mounted() {
    this.$emit(
      'selected',
      this.generateFormData(this.sectionJointList)
    );
  },
  methods: {
    generateFormData(listType) {
      return {
        section_joint_list: listType
      };
    },
  },
}
</script>