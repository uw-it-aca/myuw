<template>
  <div>
    <div v-if="showNotesOnly" class="text-dark-beige myuw-text-lg mb-3">
      {{ book.notes }}
    </div>
    <template v-else>
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
            width="80px"
            alt="Book cover image"
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
            <dt v-if="digitalItem">
              DIGITAL MATERIAL
            </dt>
            <dd v-if="digitalItem">
              <span v-if="digitalItemPaid">Paid</span>
              <span v-else-if="digitalItemOptedOut">Opted out</span>
              <span v-else>Payment due</span>
            </dd>
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
                <span v-if="book.lowest_price!=book.highest_price">
                  ${{ book.lowest_price.toFixed(2) }}
                  to
                  ${{ book.highest_price.toFixed(2) }}
                </span>
                <span v-else>
                  ${{ book.lowest_price.toFixed(2) }}
                </span>
              </div>
              <div v-if="digitalItem">Digital: ${{ digitalItem.price.toFixed(2) }}</div>
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
    </template>
  </div>
</template>

<script>
import {mapGetters, mapState} from 'vuex';
export default {
  props: {
    book: {
      type: Object,
      required: true,
    },
    sln: {
      type: Number,
      required: true,
    },
    orderUrl: {
      type: String,
      required: true,
    },
  },
  computed: {
    // MUWM-5272
    ...mapState('iac', {
      iacData(state) {
        return state.value;
      },
    }),
    ...mapGetters('iac', {
      isReady: 'isReadyTagged',
      isErrored: 'isErroredTagged',
      statusCode: 'statusCodeTagged',
    }),
    isIacReady() {
      return this.isReady && Boolean(this.iacData);
    },
    digitalItem() {
      if (this.isIacReady) {
        const iacs = this.iacData.ia_courses;
        if (iacs && this.sln in iacs) {
          const dItems = iacs[this.sln].digital_items;
          if (this.book.isbn in dItems) {
            return dItems[this.book.isbn];
          }
        }
      }
      return null;
    },
    digitalItemOptedOut() {
      if (this.digitalItem) {
        return this.digitalItem.opt_out_status;
      }
      return false;
    },
    digitalItemPaid() {
      if (this.digitalItem) {
        return this.digitalItem.paid;
      }
      return false;
    },
    formattedCoverImageUrl() {
      if (this.book.cover_image_url) {
        return `${window.location.protocol}//${this.book.cover_image_url}`;
      }
      return false;
    },
    showNotesOnly() {
      return this.book.title === 'See Notes';
    },
  },
};
</script>
