<template>
  <b-container
    fluid="xl"
    class="px-3 text-center"
    :class="[$mq == 'desktop' ? 'py-5' : 'py-3']"
  >
    <b-row class="justify-content-md-center">
      <b-col md="7">
        <b-input-group>
          <label
            class="sr-only" for="search_nav"
          >Search the UW website</label>
          <b-form-input
            id="search_nav"
            v-model="searchText"
            size="lg"
            placeholder="Search the UW website"
          />
          <b-input-group-append>
            <b-button
              :click="performSearch(searchText)"
              variant="purple"
              class="rounded-0"
            >
              <font-awesome-icon
                :icon="['fas', 'search']"
                flip="horizontal"
                class="mr-1"
              />
            </b-button>
          </b-input-group-append>
        </b-input-group>
        <div class="mt-2">Value: {{ searchText }}</div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data: function() {
    return {
      searchText: '',
      searchURL: 'https://www.washington.edu/search/?q=' + this.searchText,
    };
  },
  methods: {
    performSearch: function() {
      console.log('perform search..', this.searchURL);
    },
  },
};
</script>
