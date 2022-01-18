export default function (Vue, options) {
  if (!options) {
    options = {};
  }
  if (!options.threshold) {
    options.threshold = Array(11).fill(0).map((_, i) => i / 10);
  }

  // Checking if `IntersectionObserver` exists. Adds support for Safari 11
  let observer = null;
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          entry.target.$observer.onVisibleChange(entry);
        });
      }, options);
  }

  Vue.directive('visibility-change', {
    bind: function(el, binding) {
      if (binding.value) {
        el.$observer = {};
        el.$observer.onVisibleChange = binding.value;
        Vue.nextTick(() => {
          if (observer) observer.observe(el);
        });
      }
    },
  })
}