function linkClickHandler(event, binding, vnode, out) {
  if (event.button > 1) return;

  let label = binding.value ? binding.value : event.target.innerText;

  const instance = vnode.componentInstance ? vnode.componentInstance : vnode.context;
  // Resolves the `a` tag from the path
  const aTarget = event.target ? event.target : event.path.find((el) => el.tagName === 'A');

  instance.$logger.linkClick(
    instance,
    label,
    out,
  );

  if (out) {
    if (instance.$meta.term) {
      label += ` ${instance.$meta.term}`;
    }
    if (instance.$meta.course) {
      label += ` ${instance.$meta.course}`;
    }
    event.preventDefault();
    // Creates a clone of the original <a> so that
    // its attributes are not polluted
    const newLink = aTarget.cloneNode(true);
    newLink.href = `${document.location.origin}/out?u=${
      encodeURIComponent(aTarget.href)
    }&l=${encodeURIComponent(label)}`;

    if (event.button === 1) {
      // mouse middle button click, always open in a new window
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
        this.$el.querySelectorAll('a:not(.external-link):not(.internal-link):not([role=tab])')
          .forEach((el) => {
            // Find nearest vue component parent
            let context = null;
            for (let comp = el; comp; comp = comp.parentElement) {
              if (comp.__vue__) {
                context = comp.__vue__;
                break;
              }
            }

            if (location.hostname === el.hostname || el.hostname.length === 0) {
              el.onclick = (evt) => linkClickHandler(evt, {}, {context}, false);
              el.onauxclick = (evt) => linkClickHandler(evt, {}, {context}, false);
              el.classList.add('internal-link');
            } else {
              el.onclick = (evt) => linkClickHandler(evt, {}, {context}, true);
              el.onauxclick = (evt) => linkClickHandler(evt, {}, {context}, true);
              el.classList.add('external-link');
            }
          });
      }
    }
  });
}
