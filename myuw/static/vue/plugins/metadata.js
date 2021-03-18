export default function (Vue, options) {
  Vue.directive('meta', {
    bind: (_, binding, vnode) => {
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
        // A getter to get the nearest component that can act as a root
        // A root component either needs to start with `myuw` or it should
        // have a $meta tag value defined
        _group: null,
        get group() {
          if (this._group) return this._group;
          for (let comp=component; comp; comp = comp.$parent) {
            if (comp.$meta.tag) {
              this._group = comp;
              break;
            }
          }
          return this._group || {$meta: {tag: 'no-root-component'}};
        },
        _tag: null,
        get tag() {
          if (this._tag) return this._tag;
          if (
            component.$options._componentTag &&
            component.$options._componentTag.startsWith("myuw")
          ) {
            this._tag = component.$options._componentTag.substr(5);
            return this._tag;
          }
          return null;
        },
        set tag(val) {
          this._tag = val;
        },
        uid,
      };
      uid += 1;
    },
  });
}