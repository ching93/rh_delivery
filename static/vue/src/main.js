import Vue from 'vue'
import App from './App.vue'
import store from './store'
//import VueRouter from 'vue-router'
import buefy from 'buefy'
import 'buefy/dist/buefy.css'

Vue.use(buefy,{defaultIconPack:'fa'})

let app = new Vue({
    el: '#app',
    store,
    render: h => h(App)
});
app.$store.commit('setWindowWidth', window.innerWidth);
window.addEventListener('resize',function(e){ app.$store.commit('setWindowWidth',e.target.innerWidth)});