<script>
import { Tooltip } from 'bootstrap';

export default {
  props: {
    target: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      default: null,
    },
    placement: {
      type: String,
      default: 'top',
    },
    htmlTitle: {
      type: Boolean,
      default: false,
    },
  },
  mounted() {
    let target = document.getElementById(this.target);
    target.setAttribute('data-bs-toggle', 'tooltip');
    target.setAttribute('data-bs-placement', this.placement);

    if (this.$slots.default) {
      target.setAttribute('data-bs-html', true);
      target.setAttribute('title', this.$slots.default[0].text);
    } else {
      target.setAttribute('data-bs-html', this.htmlTitle);
      target.setAttribute('title', this.title ?? '');
    }

    let _tooltip = new Tooltip(target);
  },
  render: function (createElement) {
    return createElement('div', this.$slots ?? []);
  }
}
</script>