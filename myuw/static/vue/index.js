import { Vue, store, rootId } from './base.js'

import MyUWLayout from './containers/myuw-layout.vue'

Vue.component('myuw-layout', MyUWLayout)

new Vue({
    el: `#${rootId}`,
    created: function() {
        document.getElementById(rootId).hidden = false;
    },
    store: store,
})