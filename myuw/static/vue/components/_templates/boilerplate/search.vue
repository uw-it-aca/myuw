<template>
  <div
    class="container-xl px-3 text-center"
    :class="[$mq == 'desktop' ? 'py-5' : 'py-3']"
  >
    <div class="row justify-content-md-center">
      <div class="col-md-7">
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
              <button class="btn btn-purple rounded-0" type="submit"
              >
                <font-awesome-icon
                  :icon="faSearch"
                  flip="horizontal"
                  class="mr-1"
                />
                <span class="sr-only">Search</span>
              </button>
            </b-input-group-append>
          </b-input-group>
        </b-form>
      </div>
    </div>
  </div>
</template>

<script>
import {
  faSearch,
} from '@fortawesome/free-solid-svg-icons';

export default {
  data: function() {
    return {
      searchText: '',
      faSearch,
    };
  },
  methods: {
    performSearch: function() {
      const searchURL = 'https://www.washington.edu/search/?q=' + this.searchText;
      this.$logger.search(this.searchText);
      // navigate to uw search query
      window.location.href = searchURL;
    },
  },
};
</script>
