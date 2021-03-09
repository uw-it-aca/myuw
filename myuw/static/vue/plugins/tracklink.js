function linkClickHandler(event, binding, vnode) {
  if (event.button > 1) return;

  let label = binding.value ? binding.value :
              event.target.title ? event.target.title :
              event.target.label ? event.target.label :
              event.target.innerText ? event.target.innerText : null;

  const instance = vnode.componentInstance ? vnode.componentInstance : vnode.context;
  instance.$logger.linkClick(
    instance,
    event.target.href,
    label,
    true,
  );

  event.preventDefault();
  // Creates a clone of the original <a> so that
  // its attributes are not polluted
  const newLink = event.target.cloneNode(true);
  newLink.href = `${document.location.origin}/out?u=${
    encodeURIComponent(event.target.href)
  }&l=${encodeURIComponent(label)}`;

  if (event.button === 1) {
    newLink.target = "_blank";
  }

  newLink.click();
}

export default function(Vue, _) {
  Vue.directive('out', {
    bind: (el, binding, vnode) => {
      let bindPoint = el.tagName === 'A' ? el : el.getElementsByTagName('a')[0];
      bindPoint.addEventListener(
        'click',
        (evt) => linkClickHandler(evt, binding, vnode),
      );
      bindPoint.addEventListener(
        'auxclick',
        (evt) => linkClickHandler(evt, binding, vnode),
      );
    },
  });

  Vue.directive('out-all', {
    update: (el, binding, vnode) => {
      el.getElementsByTagName('a').forEach((el) => {
        el.addEventListener(
          'click',
          (evt) => linkClickHandler(evt, binding, vnode),
        );
        el.addEventListener(
          'auxclick',
          (evt) => linkClickHandler(evt, binding, vnode),
        );
      });
    },
  });
}