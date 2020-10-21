<template>
  <b-container
    fluid="xl"
    class="px-3 text-center"
    :class="[$mq == 'desktop' ? 'py-5' : 'py-3']"
  >
    <b-row class="justify-content-md-center">
      <b-col md="7">
        <b-form @submit.prevent="performSearch">
          <b-input-group>
            <label
              class="sr-only" for="search_nav"
            >Search the UW website</label>
            <b-form-input
              id="search_nav"
              v-model="searchText"
              size="lg"
              type="text"
              placeholder="Search the UW website"
            />
            <b-input-group-append>
              <b-button
                variant="purple"
                class="rounded-0"
                type="submit"
              >
                <font-awesome-icon
                  :icon="['fas', 'search']"
                  flip="horizontal"
                  class="mr-1"
                />
              </b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data: function() {
    return {
      searchText: '',
    };
  },
  methods: {
    performSearch: function() {
      const searchURL = 'https://www.washington.edu/search/?q=' + this.searchText;

      // console.log( window.location.pathname + '?q=' + this.searchText)

      // MARK: google analytics: log uw search queries as pageviews
      this.$gtag.pageview({
        page_path: window.location.pathname + '?q=' + this.searchText,
      });
      // navigate to uw search query
      window.location.href = searchURL;
    },
  },
};
</script>
