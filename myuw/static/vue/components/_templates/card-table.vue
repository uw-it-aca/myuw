<template>
  <!-- A responsive table supports sortable fields -->
  <div class="myuw-text-md table-responsive">
    <table
      id="student-list"
      class="table table-sm table-hover"
      cellspacing="0"
    >
      <thead class="thead-light">
        <tr>
          <th v-for="(field, index) in fields"
            :id="field.key"
            :key="index"
            :class="field.sortable ? 'b-table-sort-icon-left' : ''"
            :aria-colindex="index">
            {{ field.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(dataItems, rowIdx) in items" :key="rowIdx">
          <td v-for="(data, colIdx) in dataItems" :key="`${rowIdx}-${colIdx}`"
            :headers="data.key" :aria-colindex="colIdx">
            <slot :cellData="data" />
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
  data: function () {
    return {};
  }
}
</script>
<style lang="scss" scoped>

</style>
