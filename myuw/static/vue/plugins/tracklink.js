function linkClickHandler(event, binding, vnode, out) {
  if (event.button > 1) return;

  let label = binding.value ? binding.value :
              // event.target.title ? event.target.title :
              event.target.innerText ? event.target.innerText : null;

  const instance = vnode.componentInstance ? vnode.componentInstance : vnode.context;
  instance.$logger.linkClick(
    instance,
    event.target.href,
    label,
    out,
  );

  if (out) {
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
}

export default function(Vue, _) {
  Vue.directive('out', {
    bind: (el, binding, vnode) => {
      let bindPoint = el.tagName === 'A' ? el : el.getElementsByTagName('a')[0];
      bindPoint.onclick = (evt) => linkClickHandler(evt, binding, vnode, true);
      bindPoint.onauxclick = (evt) => linkClickHandler(evt, binding, vnode, true);
      bindPoint.classList.add('external-link');
    },
  });

  Vue.directive('out-all', {
    update: (elm, binding, vnode) => {
      elm.querySelectorAll('a:not(.external-link):not(.internal-link)').forEach((el) => {
        el.onclick = (evt) => linkClickHandler(evt, binding, vnode, true);
        el.onauxclick = (evt) => linkClickHandler(evt, binding, vnode, true);
        el.classList.add('external-link');
      });
    },
  });

  Vue.directive('inner', {
    bind: (el, binding, vnode) => {
      let bindPoint = el.tagName === 'A' ? el : el.getElementsByTagName('a')[0];
      bindPoint.onclick = (evt) => linkClickHandler(evt, binding, vnode, false);
      bindPoint.onauxclick = (evt) => linkClickHandler(evt, binding, vnode, false);
      bindPoint.classList.add('internal-link');
    },
  });

  Vue.mixin({
    updated() {
      if (this.$el && this.$el.querySelectorAll) {
        this.$el.querySelectorAll('a:not(.external-link):not(.internal-link)').forEach((el) => {
          if (location.hostname === el.hostname) {
            el.onclick = (evt) => linkClickHandler(evt, {}, {context: this}, false);
            el.onauxclick = (evt) => linkClickHandler(evt, {}, {context: this}, false);
            el.classList.add('internal-link');
          } else {
            el.onclick = (evt) => linkClickHandler(evt, {}, {context: this}, true);
            el.onauxclick = (evt) => linkClickHandler(evt, {}, {context: this}, true);
            el.classList.add('external-link');
          }
        })
      }
    }
  });
}