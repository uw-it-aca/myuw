export default {
  updated() {
    if (this.$el.querySelectorAll) {
      let links = this.$el.querySelectorAll('a:not(.out-link):not(.in-link)');
      links.forEach((link) => {
        if (link.href.includes(document.baseURI)) {
          link.classList.add('in-link');
        } else {
          let label = link.innerText;
          link.href = `${document.baseURI}out?u=${
            encodeURI(link.href)
          }&l=${encodeURI(label)}`;
          link.classList.add('out-link');
        }
      });
    }
  },
}