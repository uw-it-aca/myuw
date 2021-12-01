<template>
  <div>
    <h2 class="h5">
      {{ categoryTitle }}
    </h2>
    <ul class="list-unstyled myuw-text-md">
      <li v-for="(link, index) in links" :key="index" class="mb-1">
        <a :href="link.url">{{ link.title }}</a>
      </li>
    </ul>
  </div>
</template>

<script>

export default {
  props: {
    categoryTitle: {
      type: String,
      required: true,
    },
    links: {
      type: Array,
      required: true,
    }
  }
}
</script>
