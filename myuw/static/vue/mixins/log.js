class Logger {
  constructor(sink) {
    this.sink = sink;
  }

  card_load(component) {
    component.$nextTick(() => {
      let compTid = component.compTid;
      if (!compTid) {
        // Try to create the compTid from the card heading
        const cardHeading = component.$slots['card-heading'];
        if (
          cardHeading &&
          cardHeading[0] &&
          cardHeading[0].children &&
          cardHeading[0].children[0] &&
          cardHeading[0].children[0].text
        ) {
          compTid = cardHeading[0].children[0].text.trim();
        }
      }

      let parentCompTag = null;
      // Try to find the component tag
      for (let comp=component.$parent; comp.$parent; comp = comp.$parent) {
        if (comp.$options._componentTag.startsWith("myuw")) {
          parentCompTag = comp.$options._componentTag;
          break;
        }
      }

      if (compTid) {
        this.sink('card_load', {
          comp_tid: compTid,
          comp_tag: parentCompTag,
        });
      }
    });
  }
}

export default {
  data() {
    return {
      // Replace `this.$gtag.event` with `console.log` to log to the console
      log: new Logger(this.$gtag.event),
    }
  }
}