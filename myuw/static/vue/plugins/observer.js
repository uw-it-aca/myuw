export default function (Vue, options) {
  if (!options) {
    options = {};
  }
  if (!options.threshold) {
    options.threshold = Array(101).fill(0).map((_, i) => i / 100);
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      entry.target.$observer.onVisibleChange(entry);
    });
  }, options);
  Vue.directive('visibility-change', {
    bind: function(el, binding) {
      if (binding.value) {
        el.$observer = {};
        el.$observer.onVisibleChange = binding.value;
        Vue.nextTick(() => {
          observer.observe(el);
        });
      }
    },
  })
}