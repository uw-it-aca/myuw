<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">
      {{ book.title }}
    </h3>

    <div class="d-flex">
      <div class="me-3"
           style="min-width:80px !important; width:80px !important;"
      >
        <img
          v-if="formattedCoverImageUrl"
          :src="formattedCoverImageUrl"
          :alt="`${book.title} book cover`"
          width="80px"
          class=""
        >
        <div v-else title="No cover image available"
             class="py-5 bg-white border text-center text-muted text-uppercase
             myuw-text-md"
        >
          No<br>image
        </div>
      </div>
      <div class="flex-fill myuw-text-md">
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
            <div v-if="book.lowest_price && book.highest_price">
              ${{ book.lowest_price.toFixed(2) }}
              to
              ${{ book.highest_price.toFixed(2) }}
            </div>
            <div>
              Visit
              <a :href="orderUrl">
                ubookstore.com
              </a>
              for pricing on all available formats.
            </div>
          </dd>
          <dt v-if="book.notes">
            Notes
          </dt>
          <dd v-if="book.notes">
            <span class="text-capitalize">{{ book.notes }}</span>
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
