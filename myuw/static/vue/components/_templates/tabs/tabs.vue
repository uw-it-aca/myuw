<template>
  <div>
    <ul class="nav" :class="navClassesComputed" role="tablist">
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
    };
  },
  computed: {
    tabSlot() {
      if (this.$slots.default.length == this.ready.length) {
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
  // mounted() {
  //   console.log(this.$slots.default[this.tabIndex]);
  // },
  // render: function(createElement) {
  //   let elm = createElement('div', this.$slots.default);
  //   return elm;
  // }
}
</script>