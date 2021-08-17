<script>
import Tab from './tab.vue';

export default {
  model: {
    prop: 'tabIndex',
    event: 'selected'
  },
  props: {
    navClass: {
      type: [String, Array, Object],
      default: '',
    },
    navWrapperClass: {
      type: [String, Array, Object],
      default: '',
    },
    tabIndex: {
      type: Number,
      default: 0,
    },
    justified: {
      type: Boolean,
      default: false,
    },
    small: {
      type: Boolean,
      default: false,
    },
    pills: {
      type: Boolean,
      default: false,
    },
    bottomBorder: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      actualTabs: {},
      eventHandlers: {},
      // TODO: not used right now
      firstRender: true,
      // Unique identifier for a tab component
      tab_cid: Tab['_Ctor'][0].cid,
    };
  },
  computed: {
    navWrapperClassesComputed() {
      let wrapperClasses = this.classesToClassDict(this.navWrapperClass);

      return wrapperClasses;
    },
    navClassesComputed() {
      let navClass = this.classesToClassDict(this.navClass);
      
      if (this.pills) {
        navClass['nav-pills'] = true;
        navClass['nav-tabs'] = false;
      } else {
        navClass['nav-tabs'] = true;
        navClass['nav-pills'] = false;
      }
      if (this.justified) {
        navClass['nav-justified'] = true;
      }
      if (this.small) {
        navClass['small'] = true;
      }

      return navClass;
    }
  },
  watch: {
    actualTabs(actualTabs) {
      Object.entries(actualTabs).forEach(([id, tab]) => {
        if (!(id in this.eventHandlers)) {
          var tabEl = document
            .querySelector(`button[data-bs-toggle="tab"][data-bs-target="#${id}"]`);
          tabEl.addEventListener('show.bs.tab', (event) => {
            let selected = this.decodeId(event.target.attributes['data-bs-target'].value);
            // TODO: do i only want a one way sync?
            console.log(selected);
            // this.$emit('selected', selected.index);
            let oldSelected = this.decodeId(event.relatedTarget.attributes['data-bs-target'].value);
            this.$emit('activate-tab', selected.index, oldSelected.index, event);
          });
        }
      });
    }
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
    genId(index, groupIndex) {
      return `uw-tab-${index}-in-group-${groupIndex}`;
    },
    decodeId(id) {
      const selectGroups = id.match(/uw-tab-(\d+)-in-group-(\d+)/);
      return {index: parseInt(selectGroups[1]), group: parseInt(selectGroups[2])};
    }
  },
  render: function(createElement) {
    let liElements = [];
    let tabNodes = this.$slots.default
      .filter((child) => child.componentOptions)
      .filter((child) => child.componentOptions.Ctor.cid == this.tab_cid);
    
    tabNodes.forEach((tab, i) => {
      // Set a id for the tab
      tab.data.attrs.id = this.genId(i, this.$meta.uid);

      let li = [];
      let createButtonWith = (content) => {
        return createElement(
          'button',
          {
            class: {
              'nav-link': true,
              'text-nowrap': true,
              'text-uppercase': true,
              // TODO: This causes the whole thing to rerender when the
              // tab index is changed
              'active': this.tabIndex === i,
              ...this.classesToClassDict(tab.componentOptions.propsData.titleLinkClass),
            },
            attrs: {
              'data-bs-toggle': 'tab',
              'data-bs-target': `#${tab.data.attrs.id}`,
              'type': 'button',
              'role': 'tab',
              'aria-controls': `${tab.data.attrs.id}`,
              // TODO: This causes the whole thing to rerender when the
              // tab index is changed
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
        class: {
          nav: true,
          'myuw-tabs': true,
          'myuw-bottom-border': this.bottomBorder, 
          ...this.navClassesComputed,
        },
        attrs: {
          role: 'tablist',
        }
      },
      liElements,
    );
    let ulWrapper = createElement(
      'div',
      {
        class: this.navWrapperClassesComputed,
      },
      [ul],
    )
    // TODO: This causes the whole thing to rerender when the
    // tab index is changed
    tabNodes[this.tabIndex].data.class = {
      show: true,
      active: true,
    };

    let tabs = createElement('div', { class: { 'tab-content': true } }, this.$slots.default);
    let elm = createElement('div', [ulWrapper, tabs]);

    this.firstRender = false;
    return elm;
  },
}
</script>

<style lang="scss" scoped>
.myuw-tabs {
  .nav-link.active { 
    background: transparent;
    font-weight: bold; 
  }
}
.myuw-bottom-border {
  .nav-link { border-bottom: 0.3125rem solid #ddd; }
  .nav-link.active {
    border-bottom-color: #000;
  }
}
</style>