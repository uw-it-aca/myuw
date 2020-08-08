import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import '../css/bootstrap-theming.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

const rootId = "vue_root"
export { Vue, rootId }