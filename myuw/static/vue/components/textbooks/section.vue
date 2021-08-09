<template>
  <div>
    <div
      v-if="collapsable"
      data-toggle="collapse"
      :data-target="`#books-${section.sln}`"
      :aria-controls="`books-${section.sln}`"
      aria-expanded="false"
      aria-label="Toggle Course Textbooks"
    >
      <h2 class="h5">
        <font-awesome-icon
          :icon="faSquareFull"
          :class="`text-c${section.colorId}`"
          class="mr-1"
        />
        {{ section.curriculum }}
        {{ section.courseNumber }}{{ section.sectionId }}
      </h2>
      <div v-if="!isOpen" class="mb-3">
        {{ section.books.length }}
        {{ section.books.length > 1 ? "textbooks" : "textbook" }}
      </div>
    </div>

    <h2 v-else class="h5">
      <font-awesome-icon
        :icon="faSquareFull"
        :class="`text-c${section.colorId}`"
        class="mr-1"
      />
      {{ section.curriculum }}
      {{ section.courseNumber }}{{ section.sectionId }}
    </h2>

    <uw-collapse
      :collapsable="collapsable"
      :collapse-id="`books-${section.sln}`"
    >
      <template #collapsible>
        <div v-if="section.hasBooks" class="mb-3">
          <uw-book
            v-for="book in section.books"
            :key="`books-${section.sln}-${book.isbn}`"
            :book="book"
          />
        </div>
        <div v-else class="myuw-text-md mb-3">
          <slot name="no-books">
            No textbooks have been ordered for this course.
            <a :href="teachingOrderBookUrl">
              Order textbooks
            </a>.
          </slot>
        </div>
      </template>
    </uw-collapse>

    <hr v-if="!collapsable">
  </div>
</template>

<script>
import {
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';
import Book from './book.vue';
import Collapsible from '../_templates/collapsible.vue';

export default {
  components: {
    'uw-book': Book,
    'uw-collapse': Collapsible,
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
      faSquareFull,
      isOpen: false,
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
