<template>
  <div>
    <button
      v-uw-collapse="`books-${section.sln}`"
      :disabled="!collapsable"
      class="btn btn-link no-btn-disable-style p-0 border-0 align-top text-start myuw-text-md mb-1"
    >
      <h2 class="h5">
        <font-awesome-icon
          :icon="faSquareFull"
          :class="`text-c${section.colorId}`"
          class="me-1"
        />
        {{ section.curriculum }}
        {{ section.courseNumber }}{{ section.sectionId }}
      </h2>
      <div v-if="!section.tacomaCampus && collapsable && !isOpen" class="mb-3">
        {{ section.books.length }}
        {{ section.books.length > 1 ? "textbooks" : "textbook" }}
      </div>
    </button>
    <uw-collapse
      v-if="hasBook"
      :id="`books-${section.sln}`"
      v-model="isOpen"
    >
      <uw-book
        v-for="book in sectionBooks"
        :key="`books-${section.sln}-${book.isbn}`"
        :book="book"
        :sln="section.sln"
      />
    </uw-collapse>
    <uw-collapse
      v-else
      :id="`books-${section.sln}`"
      v-model="isOpen"
      class="myuw-text-md mb-3"
    >
      <template v-if="section.tacomaCampus">
        <a :href="viewUWTBookUrl(section)">
          Check textbooks
        </a>
      </template>
      <template v-else-if="hasNoBook">
        <span v-if="!instructor">
          No textbook requirement has been received for this course.
          Please check with your instructor.
        </span>
        <span v-else>
          No textbooks have been ordered for this course.
          <a href="https://uw.verbacollect.com/session/selfassign">
            Order textbooks
          </a>
        </span>
      </template>
      <template v-else-if="hasBookError">
        <span class="text-danger">
          No textbook data is available at this moment.
        </span>
      </template>
    </uw-collapse>

    <hr v-if="!collapsable" class="bg-secondary">
  </div>
</template>

<script>
import {
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';
import Collapse from '../_templates/collapse.vue';
import Book from './book.vue';

export default {
  components: {
    'uw-collapse': Collapse,
    'uw-book': Book,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    collapsable: {
      type: Boolean,
      default: false,
    },
    instructor: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isOpen: !this.collapsable,
      faSquareFull,
    };
  },
  computed: {
    sectionBookData() {
      return this.section && this.section.book_value;
    },
    hasBookData() {
      return this.sectionBookData && this.sectionBookData.length > 0;
    },
    hasBookError() {
      return this.hasBookData ? this.sectionBookData.error : false;
    },
    sectionBooks() {
      return this.hasBookData ? this.sectionBookData.books : [];
    },
    hasNoBook() {
      return this.sectionBooks.length == 0;
    },
    hasBook() {
      return this.sectionBooks.length > 0;
    },
  }
};
</script>

<style lang="scss" scoped>
.btn:disabled.no-btn-disable-style {
  opacity: 1.0;
}

.btn-link:disabled.no-btn-disable-style {
  color: black;
}
</style>
