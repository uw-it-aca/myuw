<template>
  <div>
    <div
      v-show="disableActions"
      class="alert alert-danger"
      role="alert"
    >
      This action is disabled while overriding as another user.
    </div>

    <fieldset class="form-group">
      <legend>
        Request multiple email lists, one for each section selected:
      </legend>
      <div class="form-check">
        <input
          id="request_multiple_checkbox"
          v-model="allSelected"
          :indeterminate.prop="indeterminate"
          class="form-check-input"
          type="checkbox"
          @change="toggleAll"
        >
        <label class="form-check-label" for="request_multiple_checkbox">
          {{ allSelected ? 'Un-Select All' : 'Select All' }}
        </label>
      </div>
      <div
        v-for="(selectable, i) in selectableEmailList"
        :key="i"
        class="form-check"
      >
        <input
          :id="`checkbox_${i}`"
          v-model="selected"
          class="form-check-input"
          type="checkbox"
          :value="selectable.value"
          :disabled="selectable.disabled"
        >
        <label class="form-check-label" :for="`checkbox_${i}`">
          {{ selectable.text }}
        </label>
      </div>
    </fieldset>
  </div>
</template>

<script>
import {mapState} from 'vuex';

function formDataToList(formData) {
  let list = [];
  Object.entries(formData).forEach(([key, label]) => list.push({key, label}));
}

function listToFormData(list) {
  let formData = {};
  list.forEach((item) => formData[item.key] = item.label);
  return formData;
}

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
      selected: formDataToList(this.formData) ?? [],
      indeterminate: false,
      allSelected: false,
    };
  },
  computed: {
    ...mapState({
      disableActions: (state) => state.disableActions,
    }),
    selectableEmailList() {
      const options = [];
      options.push({
        text: `${this.emailList.course_abbr} ${
          this.emailList.course_number
        } ${this.emailList.section_list.section_id}` + 
        (this.emailList.section_list.list_exists ? ' - List already exists' : ''),
        value: {
          key: `section_single_${this.emailList.section_list.section_id}`,
          label: this.emailList.section_list.section_label,
        },
        disabled: this.emailList.section_list.list_exists,
      });

      this.emailList.secondary_section_lists.forEach((section) => {
        options.push({
          text: `${this.emailList.course_abbr} ${
            this.emailList.course_number
          } ${section.section_id}` + 
          (section.list_exists ? ' - List already exists' : ''),
          value: {
            key: `secondary_single_${section.section_id}`,
            label: section.section_label,
          },
          disabled: section.list_exists,
        });
      });

      return options;
    }
  },
  watch: {
    selected(newValue) {
      if (newValue.length === 0) {
        this.indeterminate = false
        this.allSelected = false
      } else if (newValue.length === 
        this.selectableEmailList.filter((o) => !o.disabled).length
      ) {
        this.indeterminate = false
        this.allSelected = true
      } else {
        this.indeterminate = true
        this.allSelected = false
      }
      this.$emit('selected', listToFormData(newValue));
    }
  },
  methods: {
    toggleAll(evt) {
      this.selected = evt.target.checked ?
        this.selectableEmailList.filter((o) => !o.disabled).map((o) => o.value) : [];
    },
  },
}
</script>