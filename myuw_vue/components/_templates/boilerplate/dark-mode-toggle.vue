<template>
  <span>
    <input type="checkbox" id="dark-mode-button" name="dark-mode" v-model="checked">
    <label class="text-white" for="dark-mode">Enable Dark Mode</label><br>
  </span>
</template>

<script>
export default {
  data: function() {
    return {
      checked: false,
    };
  },
  created() {
    if (localStorage.theme) {
      this.checked = localStorage.theme === "dark";
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      this.checked = true;
    }
  },
  watch: {
    checked() {
      let theme = this.checked ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.theme = theme;
    }
  },
};
</script>
