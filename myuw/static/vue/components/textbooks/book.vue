<template>
  <div>
    <h4>{{ book.title }}</h4>
    <img
      v-if="formattedCoverImageUrl"
      :src="formattedCoverImageUrl"
      :alt="`${book.title} book cover`"
      width="80px"
    >
    <div v-else title="No cover image available">
      No Image Available
    </div>
    <div>
      <dl>
        <dt>
          {{ book.authors > 1 ? "Authors" : "Author" }}
        </dt>
        <dd
          v-for="(author, i) in book.authors"
          :key="`book-${book.isbn}-author-${i}`"
        >
          {{ author.name }}
        </dd>
        <dt>Price </dt>
        <dd>
          <p v-if="book.lowest_price && book.highest_price">
            {{ book.lowest_price.toFixed(2) }}
            to
            {{ book.highest_price.toFixed(2) }}
          </p>
          <p>
            Visit
            <a target="_blank" :href="orderUrl">
              ubookstore.com
            </a>
            for pricing on all available formats.
          </p>
        </dd>
        <dt v-if="book.notes">
          Notes
        </dt>
        <dd v-if="book.notes">
          {{ book.notes }}
        </dd>
        <dt v-if="book.isbn">
          ISBN
        </dt>
        <dd v-if="book.isbn">
          {{ book.isbn }}
        </dd>
      </dl>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    book: {
      type: Object,
      required: true,
    },
  },
  computed: {
    formattedCoverImageUrl() {
      if (this.book.cover_image_url) {
        return `${window.location.protocol}//${this.book.cover_image_url}`;
      }
      return false;
    },
    orderUrl() {
      if (this.book.order_url) {
        return this.book.order_url;
      }
      return 'http://www.ubookstore.com/adoption-search';
    },
  },
};
</script>
