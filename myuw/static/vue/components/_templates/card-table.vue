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
            ref="fields"
            :key="index"
            :class="sortTheadThClasses(field)"
            aria-sort="none"
            :aria-colindex="index"
          >
            <a v-if="field.sortable" href="#"
              :title="`Sort table content by ${field.label}`"
              style="text-decoration: none; color: #495057"
              @click="sortByCol(field.key, index)"
            >{{ field.label }}</a>
            <span v-else>{{ field.label }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(dataItems, rowIdx) in renderedItems" :key="rowIdx">
          <td v-for="(value, name, colIdx) in dataItems" :key="`${rowIdx}-${name}`"
            :headers="name" :aria-colindex="colIdx">
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
  data() {
    return {
      // A shallow clone so that we don't modify the prop
      renderedItems: [...this.items],
    };
  },
  watch: {
    // Used to sync the renderedItems copy
    items(newValue) {
      this.renderedItems = [...newValue];
      let sortedBy = this.sortedBy();

      if (sortedBy) {
        this.sortByCol(sortedBy.id, sortedBy.getAttribute('aria-colindex'));
      }
    }
  },
  methods: {
    sortTheadThClasses(field) {
      // methods to compute classes for thead>th cells
      const v = ['text-nowrap', 'sticky-header'];
      if (field.sortable) {
        v.push('sort-icon-left');
      }
      return v.join(' ');
    },
    sortedBy() {
      return this.$refs['fields']
        .find((field) => field.attributes['aria-sort'].value != 'none');
    },
    sortByCol(key, index) {
      let sortedBy = this.sortedBy();

      // Clear current sorted
      if (sortedBy) {
        if (sortedBy.id == key) {
          if (sortedBy.attributes['aria-sort'].value == 'ascending') {
            sortedBy.attributes['aria-sort'].value = 'descending';
          } else if (sortedBy.attributes['aria-sort'].value == 'descending') {
            sortedBy.attributes['aria-sort'].value = 'ascending';
          } else {
            console.error(
              'aria-sort in invalid state: ',
              sortedBy.attributes['aria-sort'],
              ' for element: ',
              sortedBy,
            );
          }
        } else {
          sortedBy.attributes['aria-sort'].value = 'none';
          this.$refs['fields'][index].attributes['aria-sort'].value = 'ascending';
        }
      } else {
        this.$refs['fields'][index].attributes['aria-sort'].value = 'ascending';
      }

      let direction = this.$refs['fields'][index]
          .attributes['aria-sort'].value == 'ascending' ? 1 : -1;
      
      // We only want to sort on the renderedItems becuase this.items is a
      // prop and should not be modified
      this.renderedItems.sort((a, b) => {
        return direction * this.defaultSortCompare(
          a,
          b,
          { sortByField: key, nullLast: true },
        );
      });
    },
  },
}
</script>
<style lang="scss" scoped>
.sort-icon-left {
  background-position: left .0rem center;
  background-repeat: no-repeat;
  padding-left: calc(.75rem + .1rem);
  background-size: .65em 1em;

  &[aria-sort="none"] {
    background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='101' height='101' view-box='0 0 101 101' preserveAspectRatio='none'><path fill='black' opacity='.3' d='M51 1l25 23 24 22H1l25-22zM51 101l25-23 24-22H1l25 22z'/></svg>");
  }
  
  &[aria-sort="ascending"] {
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='101' height='101' view-box='0 0 101 101' preserveAspectRatio='none'><path fill='black' d='M51 1l25 23 24 22H1l25-22z'/><path fill='black' opacity='.3' d='M51 101l25-23 24-22H1l25 22z'/></svg>");
  }

  &[aria-sort="descending"] {
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='101' height='101' view-box='0 0 101 101' preserveAspectRatio='none'><path fill='black' opacity='.3' d='M51 1l25 23 24 22H1l25-22z'/><path fill='black' d='M51 101l25-23 24-22H1l25 22z'/></svg>");
  }
}
.sticky-header {
  position: sticky;
  top: 0;
  z-index: 2;
}
</style>
