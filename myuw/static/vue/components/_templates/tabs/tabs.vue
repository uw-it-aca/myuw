<template>
  <div>
    <ul class="nav myuw-tabs" :class="navClassesComputed" role="tablist">
      <slot />
    </ul>
    <slot-content :node="tabSlot" />
  </div>
</template>

<script>
import SlotContent from './slot-content.vue';

export default {
  components: {
    'slot-content': SlotContent,
  },
  model: {
    prop: 'tabIndex',
    event: 'selected'
  },
  props: {
    navWrapperClass: {
      type: String,
      default: '',
    },
    activeNavItemClass: {
      type: String,
      default: '',
    },
    tabIndex: {
      type: Number,
      default: 0,
    },
    pills: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      ready: [],
      rerender: false,
    };
  },
  computed: {
    tabSlot() {
      this.rerender;
      if (this.$slots.default.filter((i) => i.tag?.includes('uw-tab')).length == this.ready.length) {
        return this.$slots
          .default[this.tabIndex]
          .componentInstance
          .$slots
          .default;
      }
      return [];
    },
    navClassesComputed() {
      let wrapperClasses = this.navWrapperClass;
      
      if (this.pills) {
        wrapperClasses += ' nav-pills';
      } else {
        wrapperClasses += ' nav-tabs';
      }

      return wrapperClasses;
    }
  },
  mounted() {
    console.log(this.$slots);
  },
  // render: function(createElement) {
  //   let elm = createElement('div', this.$slots.default);
  //   return elm;
  // }
}
</script>

<style lang="scss">
.myuw-tabs {
  .nav-link { border-bottom: 0.3125rem solid #ddd; }
  .nav-link.active { 
    background: transparent;
    font-weight: bold; 
    border-bottom-color: #000;
  }
}
</style>