import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        customer: null,
        loading: false,
        orders: [],
        orderFormDesc: {},
        windowWidth: 2000,
        charCount: 10
    },
    actions: {
    },
    mutations: {
        setWindowWidth(state, width) {
            state.windowWidth = width;
            if (width > 1700)
                state.charCount = 35;
            else if (width > 1600)
                state.charCount = 30;
            else if (width > 1450)
                state.charCount = 20;
            else if (width > 1330)
                state.charCount = 15;
            else if (width > 1200)
                state.charCount = 10;
            else if (width > 1010)
                state.charCount = 6;
        },
        setCustomer(state, payload) {
            state.customer = payload;
        },
        toggleLoading(state) {
            state.loading = !state.loading;
        },
        showLoading(state) {
            state.loading = true;
        },
        hideLoading(state) {
            state.loading = false;
        },
        loadOrders(state, data) {
            state.orders = data.orders;
            state.orderFormDesc = data.orderFormDesc;
        },
        addOrder(state, order) {
            state.orders.push(order);
        },
        addOrders(state, orders) {
            for (let order of orders)
                state.orders.push(order);
        },
        replaceOrder(state, index, order) {
            state.orders.splice(index, 1, order);
        },
        updateOrder(state, {key, value, pk}) {
            let order = state.orders.filter((o)=>o.pk === pk)[0];
            if (!order)
                throw Error('no order with pk='+pk);
            let index = state.orders.indexOf(order);
            order[key] = value;
            state.orders.splice(index, 1, order);
        }
    }
});