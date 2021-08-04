<template>
  <!-- A responsive table supports sortable fields -->
  <div class="myuw-text-md table-responsive">
    <table
      id="student-list"
      class="table table-sm table-hover"
      :aria-colcount="fields.length"
    >
      <thead class="thead-light">
        <tr>
          <th v-for="(field, index) in fields"
            :id="field.key"
            :key="index"
            :class="sortTheadThClasses(field)"
            :aria-sort="sortTheadThAttrs(field)"
            :aria-colindex="index + 1"
          >
            <a v-if="field.sortable" href="#" @click="sortCol(field)"
            >{{ field.label }}<span class="sr-only">(Click to sort)</span>
            </a>
            <span v-else>{{ field.label }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(dataItems, rowIdx) in items" :key="rowIdx">
          <td v-for="(value, name, colIdx) in dataItems" :key="`${rowIdx}-${name}`"
            :headers="name" :aria-colindex="colIdx + 1">
            <slot :cellData="{key: name, value: value}" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    // table heading fields
    fields: {
      type: Array,
      required: true,
    },
    // table contents: a list of cell data items
    items: {
      type: Array,
      required: true,
    }
  },
  data: function() {
return {
      localSortBy: '',
      localSortDesc: false,
  };
},
  computed: {
  },
  methods: {
    sortTheadThAttrs(field) {
      if (field.sortable) {
        if (this.localSortBy === field.key) {
          return this.localSortDesc ? 'descending' : 'ascending';
        }
        return 'none';
      }
      return "";
    },
    sortTheadThClasses(field) {
      // methods to compute classes for thead>th cells
      const v = ['sticky-header'];
      if (field.sortable) {
        v.push('sort-icon-left');
      }
      return v.join(' ');
    },
    sortCompare(a, b) {
      return this.defaultSortCompare(a, b, { sortByField: this.localSortBy });
    },
    sortCol(field) {
      this.localSortBy = field.key;
      this.items = this.items.sort(this.sortCompare);
      this.localSortDesc = !this.localSortDesc;
    },
  }
}
</script>
<style lang="scss" scoped>
 // $b-table-sort-icon-bg-width: 0.65em !default;
 // $b-table-sort-icon-bg-height: 1em !default;
 // Sort icons are square, but "squished" horizontally by the above variables
 // b-table-sort-icon-bg-not-sorted: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='101' height='101' view-box='0 0 101 101' preserveAspectRatio='none'><path fill='black' opacity='.3' d='M51 1l25 23 24 22H1l25-22zM51 101l25-23 24-22H1l25 22z'/></svg>") !default;
 // b-table-sort-icon-bg-ascending: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='101' height='101' view-box='0 0 101 101' preserveAspectRatio='none'><path fill='black' d='M51 1l25 23 24 22H1l25-22z'/><path fill='black' opacity='.3' d='M51 101l25-23 24-22H1l25 22z'/></svg>") !default;
 // b-table-sort-icon-bg-descending: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='101' height='101' view-box='0 0 101 101' preserveAspectRatio='none'><path fill='black' opacity='.3' d='M51 1l25 23 24 22H1l25-22z'/><path fill='black' d='M51 101l25-23 24-22H1l25 22z'/></svg>") !default;
 // > [aria-sort="none"] {
 //    background-image: bv-escape-svg($b-table-sort-icon-bg-not-sorted);
 //   }
 // > [aria-sort="ascending"] {
 //   background-image: bv-escape-svg($b-table-sort-icon-bg-ascending);
 //   }
 // > [aria-sort="descending"] {
 //   background-image: bv-escape-svg($b-table-sort-icon-bg-descending);
 //   }
  .sort-icon-left {
  // background-position: left calc(#{$table-cell-padding} / 2) center;
  // padding-left: calc(#{$table-cell-padding} + #{$b-table-sort-icon-bg-width});
  }
  .sticky-header {
    position: sticky;
    top: 0;
    z-index: 2;
  }
</style>
