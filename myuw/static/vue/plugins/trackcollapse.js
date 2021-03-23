function linkClickHandler(_event, el, vnode) {
	const label = el.innerText ? el.innerText.trim() : null;
	const instance = vnode.componentInstance ? vnode.componentInstance : vnode.context;
	if (el.classList.contains('collapsed')) {
		instance.$logger.disclosureOpen(instance, label);
	}
}

export default function(Vue, _) {
	// Should be put on the button
	Vue.directive('no-track-collapse', {
		bind: (el, _binding, _vnode) => {
			const elm = el.tagName === 'BUTTON' ? el :
				el.querySelector('button:is(.collapsed,.not-collapsed):not(.no-track-collapse)');
			
			if (elm) {
				elm.classList.add('no-track-collapse');
			}
		},
	});
  
	Vue.mixin({
		updated() {
			if (this.$el && this.$el.querySelectorAll) {
				this.$el.querySelectorAll(
					'button:is(.collapsed,.not-collapsed):not(.no-track-collapse):not(.track-collapse)'
				).forEach((el) => {
					// Find nearest vue component parent
					let context = null;
					for (let comp = el; comp; comp = comp.parentElement) {
						if (comp.__vue__) {
							context = comp.__vue__;
							break;
						}
					}

					el.onclick = (evt) => linkClickHandler(evt, el, {context});
					el.classList.add('track-collapse');
				});
			}
		}
	});
  }