export default function (Vue, options) {
  /**
   * Sets the meta attributes for a component
   * Attributes used by the logger
   * - tag (String) The component tag
   * - groupRoot (Boolean) If the component should be treated as the root
   *                       for a group of all its children
   *                       (TODO: Deprecate this in favor of `tag`
   *                        automatically indicating group root)
   * - term (String) If the data in a component depends on a term
   * - course (String) If the data in a component depends on a course
   */
  Vue.directive('meta', {
    bind: (_, binding, vnode) => {
      if (binding.value) {
        Object.entries(binding.value).forEach(([key, value]) => {
          vnode.context.$meta[key] = value;
        });
      }
    },
    update: (_, binding, vnode) => {
      if (binding.value) {
        Object.entries(binding.value).forEach(([key, value]) => {
          vnode.context.$meta[key] = value;
        });
      }
    },
  });

  let uid = 0;

  Vue.mixin({
    beforeCreate() {
      const component = this;
      this.$meta = {
        resolveComputedFields(comp) {
          if (
            !this._tag &&
            comp.$options._componentTag &&
            comp.$options._componentTag.startsWith("myuw")
          ) {
            this._tag = comp.$options._componentTag.substr(5);
            comp.$el.id = comp.$options._componentTag;
          }

          if (!this._group && (this.groupRoot || this._tag)) {
            this._group = comp;
          }

          if (!this._group) {
            const parent = comp.$parent;
            if (!parent) return;

            if (parent.$meta.groupRoot && parent.$meta.tag) {
              this._group = parent;
            } else if (parent.$meta.group) {
              this._group = parent.$meta.group;
            }

            if (!this._course && parent.$meta.course) {
              this._course = parent.$meta.course;
            }

            if (!this._term && parent.$meta.term) {
              this._term = parent.$meta.term;
            }
          }
        },
        _course: null,
        get course() {
          if (this._course) return this._course;
          this.resolveComputedFields(component);
          return this._course;
        },
        set course(value) {
          this._course = value;
        },
        // A getter to get the nearest component that can act as a root
        // A root component either needs to start with `myuw` or it should
        // have a $meta tag value defined
        _group: null,
        get group() {
          if (this._group) return this._group;
          this.resolveComputedFields(component);
          return this._group || {$meta: {tag: 'no-root-component'}};
        },
        _tag: null,
        get tag() {
          if (this._tag) return this._tag;
          this.resolveComputedFields(component);
          return null;
        },
        set tag(val) {
          this._tag = val;
        },
        _term: null,
        get term() {
          if (this._term) return this._term;
          this.resolveComputedFields(component);
          return this._term;
        },
        set term(value) {
          this._term = value;
        },
        uid,
      };
      uid += 1;
    },
  });
}