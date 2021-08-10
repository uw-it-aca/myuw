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
      <div v-if="collapsable && !isOpen">
        {{ section.books.length }}
        {{ section.books.length > 1 ? "textbooks" : "textbook" }}
      </div>
    </button>
    <uw-collapse
      v-if="section.hasBooks"
      :id="`books-${section.sln}`"
      v-model="isOpen"
    >
      <uw-book
        v-for="book in section.books"
        :key="`books-${section.sln}-${book.isbn}`"
        :book="book"
      />
    </uw-collapse>
    <uw-collapse
      v-else
      :id="`books-${section.sln}`"
      v-model="isOpen"
      class="myuw-text-md"
    >
      <slot name="no-books">
        No textbooks have been ordered for this course.
        <a :href="teachingOrderBookUrl">
          Order textbooks
        </a>.
      </slot>
    </uw-collapse>

    <hr v-if="!collapsable">
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
  },
  data() {
    return {
      isOpen: !this.collapsable,
      faSquareFull,
    };
  },
  computed: {
    teachingOrderBookUrl() {
      let baseUrl = 'http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=';
      if (this.section.bothellCampus) {
        baseUrl += 'uwbothell';
      } else if (this.section.tacomaCampus) {
        baseUrl += 'uwtacoma';
      } else {
        baseUrl += 'uwmain';
      }
      return baseUrl;
    },
  },
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
