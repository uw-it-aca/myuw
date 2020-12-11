<template>
  <div>
    <div id="classlist_controls">
      <div role="tablist" aria-label="Views">
        <div>
          <a id="list_view"
             href="#" role="tab"
             aria-controls="classlist_table_view"
             aria-selected="true"
          >
            <i class="fa fa-table" aria-hidden="true" />Table
          </a>
        </div>

        <div>
          <a id="grid_view"
             href="#" role="tab"
             aria-controls="classlist_photo_view"
             aria-selected="false"
          >
            <i class="fa fa-user-circle-o" aria-hidden="true" />Photo Grid
          </a>
        </div>
      </div>

      <div>
        <div id="classlist-sort-controls">
          <label for="sort_list">Sort: </label>
          <select id="sort_list" class="">
            <option value="surname,first_name" selected="selected">
              Last Name
            </option>
            <option value="first_name,surname">
              First Name
            </option>
            <option value="netid">
              UW NetID
            </option>
            <option value="class_code">
              Class
            </option>
            <option value="credits">
              Credits
            </option>
            <option v-if="section.has_linked_sections"
                    value="linked_sections"
            >
              Secondary Section
            </option>
          </select>
        </div>

        <button v-if="section.has_joint"
                id="toggle_joint"
                type="button" class=""
                aria-pressed="false"
                title="Show students from joint courses"
        >
          <i class="fa fa-square-o" aria-hidden="true" />
          Joint Course Students
        </button>
      </div>

      <div class="">
        <a id="download_class_list" href="#" class="">
          <i class="fa fa-download" />Download (CSV)
        </a>

        <a href="javascript:window.print()" class="">
          <i class="fa fa-print" />Print
        </a>
      </div>
    </div>

    <uw-table-view :section="section" />

    <uw-photo-list :registrations="section.registrations" />
  </div>
</template>

<script>
import TableView from './table-view.vue';
import PhotoList from './photo-list.vue';

export default {
  components: {
    'uw-table-view': TableView,
    'uw-photo-list': PhotoList,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    section: {
      type: Object,
      required: true,
    },
  },
  methods: {

  },
};
</script>
