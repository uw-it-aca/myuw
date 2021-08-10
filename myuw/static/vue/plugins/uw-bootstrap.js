function getTarget(binding) {
  return binding.value ??
    Object.entries(binding.modifiers).filter(([_, b]) => b)[0][0];
}

export default function(Vue, _) {
  Vue.directive('uw-collapse', {
    bind: (el, binding) => {
      let target = getTarget(binding);

      // set the attributes required by bootstrap
      el.setAttribute('data-bs-toggle', 'collapse');
      el.setAttribute('data-bs-target', `#${CSS.escape(target)}`);
      el.setAttribute('aria-expanded', 'false');
      el.setAttribute('aria-controls', target);
      el.setAttribute('role', 'button');
    },
  });

  Vue.directive('uw-modal', {
    bind: (el, binding) => {
      let target = getTarget(binding);

      // set the attributes required by bootstrap
      el.setAttribute('data-bs-toggle', 'modal');
      el.setAttribute('data-bs-target', `#${CSS.escape(target)}`);
      el.setAttribute('role', 'button');
    },
  });
}