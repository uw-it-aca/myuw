import {Vue, vueConf} from './base.js';

import Boilerplate from './containers/boilerplate.vue';

vueConf.store.state['pageTitle'] = "Accounts";

Vue.component('myuw-boilerplate', Boilerplate)

new Vue({
	...vueConf,
});
