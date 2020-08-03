import Vue from 'vue'
import Home from '../pages/home.vue'
import SideCard from '../components/sidecard.vue'

Vue.component('home-page-component', Home)
Vue.component('side-card-component', SideCard)

new Vue({ el: '#landing-vue' })