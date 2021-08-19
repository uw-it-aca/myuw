<script>
import { Tab } from 'bootstrap';
import UwTab from './tab.vue';

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
      tab_cid: UwTab['_Ctor'][0].cid,
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
      Object.entries(actualTabs).forEach(([id, tab], i) => {
        if (!(id in this.eventHandlers)) {
          var tabEl = document
            .querySelector(`button[data-bs-toggle="tab"][data-bs-target="#${id}"]`);
          tabEl.addEventListener('show.bs.tab', (event) => {
            let selected = this.decodeId(event.target.attributes['data-bs-target'].value);
            let oldSelected = this.decodeId(event.relatedTarget.attributes['data-bs-target'].value);
            this.$emit('activate-tab', selected.index, oldSelected.index, event);
            this.$nextTick(() => {
              if (!event.defaultPrevented) {
                this.$emit('selected', selected.index);
              }
            });
          });
        }
      });
    },
  },
  mounted() {
    document.addEventListener('keydown', (keyEvt) => {
      if (document.activeElement?.getAttribute('data-bs-target')?.substr(1) in this.actualTabs) {
        let current = this.tabIndex;
        if (keyEvt.key === 'ArrowLeft' && current > 0) {
          current -= 1;
        } else if (keyEvt.key === 'ArrowRight' && current < Object.keys(this.actualTabs).length - 1) {
          current += 1;
        }
        if (current != this.tabIndex) {
          var tabEl = document
            .querySelector(`button[data-bs-toggle="tab"][data-bs-target="#${this.genId(current, this.$meta.uid)}"]`);
          tabEl.focus();
          let tab = Tab.getOrCreateInstance(tabEl);
          tab.show();
        }
      }
    });
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
    },
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
              'tabindex': this.tabIndex === i ? 0 : -1,
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
    );

    let tabs = null;
    if (this.firstRender) {
      tabNodes[this.tabIndex].data.class = {
        show: true,
        active: true,
      };
      tabs = [createElement('div', { class: { 'tab-content': true } }, this.$slots.default)];
    } else {
      tabs = [createElement('div', { class: { 'tab-content': true } }, tabNodes)];
    }
    let elm = createElement('div', [ulWrapper].concat(tabs));

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