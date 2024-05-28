/*
 * Defer image loading until the parent element enters the viewport.
 *
 * Component code:
 *
 *   <template>
 *     <div v-lazyload>
 *       <img :data-url="{image_url}" />
 *     </div>
 *   </template>
 *
 *   <script>
 *     import LazyLoad from "@/directives/lazyload";
 *
 *     export default {
 *       directives: {
 *         lazyload: LazyLoad,
 *       },
 *     };
 *   </script>
 */
export default {
  bind: el => {  // Vue 2.7
  // mounted: el => {   with Vue 3
    function loadImage() {
      const imageElement = Array.from(el.children).find(
        el => el.nodeName === "IMG"
      );
      if (imageElement) {
        imageElement.src = imageElement.dataset.url;
      }
    }

    function handleIntersect(entries, observer) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadImage();
          observer.unobserve(el);
        }
      });
    }

    function createObserver() {
      const options = {
        root: null,
        threshold: "0"
      };
      const observer = new IntersectionObserver(handleIntersect, options);
      observer.observe(el);
    }

    if (window["IntersectionObserver"]) {
      createObserver();
    } else {
      loadImage();
    }
  }
};
