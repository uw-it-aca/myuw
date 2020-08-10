import "core-js/stable";
import "regenerator-runtime/runtime";
import Vue from 'vue'
import Vuex from 'vuex'

import '../css/bootstrap-theming.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        user: JSON.parse(document.getElementById('user').innerHTML),
    }
})

const rootId = "vue_root"
export { Vue, store, rootId }