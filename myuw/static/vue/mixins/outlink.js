export default {
  updated() {
    if (this.$el.querySelectorAll) {
      let links = this.$el.querySelectorAll('a:not(.out-link):not(.in-link)');
      links.forEach((link) => {
        if (link.href.includes(document.location.origin)) {
          link.classList.add('in-link');
        } else {
          if (link.href !== "") {
            let label = link.innerText;
            link.href = `${document.location.origin}/out?u=${
              encodeURIComponent(link.href)
            }&l=${encodeURIComponent(label)}`;
            link.classList.add('out-link');
          }
        }
      });
    }
  },
}