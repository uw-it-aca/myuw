<template>
  <div>
    <div v-b-toggle="`books-${section.sln}`" :disabled="!collapsable">
      <h3 class="h4">
        <font-awesome-icon
          :icon="['fas', 'square-full']"
          :class="`text-c${section.colorId}`"
          class="mr-1"
        />
        {{ section.curriculum }}
        {{ section.courseNumber }}{{ section.sectionId }}
      </h3>
      <div v-if="collapsable && !isOpen">
        {{ section.books.length }}
        {{ section.books.length > 1 ? "textbooks" : "textbook" }}
      </div>
    </div>
    <b-collapse
      v-if="section.hasBooks"
      :id="`books-${section.sln}`"
      v-model="isOpen"
    >
      <uw-book
        v-for="book in section.books"
        :key="`books-${section.sln}-${book.isbn}`"
        :book="book"
      />
    </b-collapse>
    <b-collapse
      v-else
      :id="`books-${section.sln}`"
      v-model="isOpen"
    >
      <slot name="no-books">
        No textbooks have been ordered for this course.
        <a :href="teachingOrderBookUrl">
          Order textbooks
        </a>.
      </slot>
    </b-collapse>

    <hr v-if="!collapsable">
  </div>
</template>

<script>
import Book from './book.vue';

export default {
  components: {
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
    };
  },
  computed: {
    teachingOrderBookUrl() {
      let baseUrl = 'http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=';
      if (this.section.bothell_campus) {
        baseUrl += 'uwbothell';
      } else if (this.section.tacoma_campus) {
        baseUrl += 'uwtacoma';
      } else {
        baseUrl += 'uwmain';
      }
      return baseUrl;
    },
  },
};
</script>
