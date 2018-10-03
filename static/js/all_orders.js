Vue.component('tab-all-orders', {
    delimiters: ["[[","]]"],
    template: `
    <div>
        <table class="table">
        <thead>
            <tr v-if="orders.length > 0"><th v-for="(value,key) in orders[0]">[[key]]</th></tr>
        </thead>
        <tbody>
        <tr v-for="order in orders">
            <td v-for="(value,key) in order">[[value]]</td>
        </tr>
        </tbody>
        </table><input type="hidden" v-model:value="loadList">
    </div>
    `,
    data: function(){
        return {
            orders: []
        }
    },
    methods: {
        loadOrders() {
            let url = "/delivery/all/";
            $.ajax({url: url, method: "GET", data: {}, success: this.showResponse, error: this.showError});
        },
        showResponse(data) {
            this.orders = data.orders;
        },
        showError(data) {
            $("#msg-log").html(data.message);
        }
    },
    props: {
        load: {type: Boolean, default: true }
    },
    computed: {
        loadList() {
            if (this.load == true) {
                this.loadOrders();
                this.load = false;
            }
        }
    }
});