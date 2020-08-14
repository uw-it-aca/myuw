import { Vue, store, rootId } from './base.js'

import Boilerplate from './containers/boilerplate.vue'

store.state['pageTitle'] = "Teaching";

Vue.component('myuw-boilerplate', Boilerplate)

new Vue({
    el: `#${rootId}`,
    created: function() {
        document.getElementById(rootId).hidden = false;
    },
    store: store,
})