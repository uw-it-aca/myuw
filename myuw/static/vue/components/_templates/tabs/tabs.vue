<script>
import Tab from './tab.vue';

export default {
  model: {
    prop: 'tabIndex',
    event: 'selected'
  },
  props: {
    navWrapperClass: {
      type: [String, Array, Object],
      default: '',
    },
    activeNavItemClass: {
      type: [String, Array, Object],
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
      actualTabs: {},
      // Unique identifier for a tab component
      tab_cid: Tab['_Ctor'][0].cid,
    };
  },
  computed: {
    navClassesComputed() {
      let wrapperClasses = this.classesToClassDict(this.navWrapperClass);
      
      if (this.pills) {
        wrapperClasses['nav-pills'] = true;
      } else {
        wrapperClasses['nav-tabs'] = true;
      }

      return wrapperClasses;
    }
  },
  mounted() {
    
  },
  methods: {
    classesToClassDict(classes) {
      let classDict = {};

      if (classes instanceof String || typeof(classes) === 'string') {
        classes.split(/\s+/).forEach((c) => classDict[c] = true);
      } else if (classes instanceof Array) {
        classes.forEach((c) => classDict[c] = true);
      } else if (classes) {
        // Want to copy here?
        Object.entries(classes).forEach(([key, value]) => classDict[key] = value);
      }

      return classDict;
    },
  },
  render: function(createElement) {
    let liElements = [];
    let tabNodes = this.$slots.default
      .filter((child) => child.componentOptions)
      .filter((child) => child.componentOptions.Ctor.cid == this.tab_cid);
    
    tabNodes.forEach((tab, i) => {
      // Set a id for the tab
      tab.data.attrs.id = `uw-tab-${i}-in-group-${this.$meta.uid}`;

      let li = [];
      let createButtonWith = (content) => {
        return createElement(
          'button',
          {
            class: {
              'nav-link': true,
              'text-nowrap': true,
              'text-uppercase': true,
              'active': this.tabIndex === i,
              ...this.classesToClassDict(tab.componentOptions.propsData.titleLinkClass),
            },
            attrs: {
              'data-bs-toggle': 'tab',
              'data-bs-target': `#${tab.data.attrs.id}`,
              'type': 'button',
              'role': 'tab',
              'aria-controls': `${tab.data.attrs.id}`,
              'aria-selected': this.tabIndex === i,
            },
          },
          content,
        );
      };
      let createLiWith = (content) => {
        return createElement(
          'li',
          {
            class: {
              'nav-item': true,
              ...this.classesToClassDict(tab.componentOptions.propsData.titleItemClass),
            },
            attrs: {
              role: 'presentation',
            },
          },
          content,
        );
      };

      if (tab.data.attrs.id in this.actualTabs) {
        let realTab = this.actualTabs[tab.data.attrs.id];

        if (realTab.$slots['title-no-button']) {
          li = createLiWith([realTab.$slots['title-no-button']]);
        } else if (realTab.$slots.title) {
          li = createLiWith([createButtonWith(realTab.$slots.title)]);
        } else {
          li = createLiWith([createButtonWith(realTab.title)]);
        }
      } else {
        li = createLiWith([createButtonWith("")]);
      }

      liElements.push(li);
    });

    let ul = createElement(
      'ul',
      {
        class: { nav: true, 'myuw-tabs': true, ...this.navClassesComputed },
      },
      liElements,
    );
    tabNodes[this.tabIndex].data.class = {
      show: true,
      active: true,
    };
    let tabs = createElement('div', { class: { 'tab-content': true } }, this.$slots.default);
    let elm = createElement('div', [ul, tabs]);
    return elm;
  },
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