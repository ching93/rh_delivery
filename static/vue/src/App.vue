<template>
    <div class="main">
        <b-loading is-full-page :active="$store.state.loading"></b-loading>
        <div class="columns is-multiline" style="width: 100%">
            <div class="column is-half has-text-left">
                <button class="button is-primary" v-on:click="show_create_modal=true">Новый заказ</button>
                <button class="button is-primary" v-on:click="show_driver_modal=true">Новый водитель</button>
                <b-tooltip label="yessss!"><button class="button is-primary" @click="show_excel_modal=true">Загрузка заявок с таблицы Excel</button></b-tooltip>
                <button class="button is-primary" @click="show_raworder_modal=true" v-if="incorrectRows.length > 0">Загруженные заявки</button>
                <b-modal :active.sync="show_excel_modal" has-modal-card>
                    <div class="modal-card">
                        <div class="modal-card-head">
                            <h5 class="modal-card-title">Загрузка списка заявок с таблицы Excel</h5>
                        </div>
                        <div class="modal-card-body">
                            <b-field label="Выберите файл" class="file">
                                <b-upload v-model="excel_file" size="is-small">
                                    <a class="button is-primary "><b-icon pack="fas" icon="upload"></b-icon>Открыть</a>
                                </b-upload>
                                <span class="control file-name" v-if="excel_file.length > 0">{{excel_file[0].name}}</span>
                            </b-field>
                        </div>
                        <div class="modal-card-foot">
                            <button class="button" @click="show_excel_modal=false">Закрыть</button>
                            <button class="button" @click="sendExcel">Отправить</button>
                        </div>
                    </div>
                </b-modal>
            </div>
            <div class="column is-half has-text-right">

                <b-field label="Выберите клиента:" custom-class="is-narrow " :type="$store.state.customer==null ? 'is-danger' : 'is-primary'">
                    <suggest v-bind:select-url="customerAutocompleteUrl" name="customer" class="is-pulled-right"
                             v-on:change-row="$store.commit('setCustomer',$event)" ></suggest>
                </b-field>
                <orders-from-excel :incorrect-rows="incorrectRows"
                                   :total-rows="totalRows"
                                   :saved-rows="savedRows"
                                   :ignored-rows="ignoredRows"
                                   :active.sync="show_raworder_modal"></orders-from-excel>
            </div>
            <div class="columns rh-col">
                <div class="column">
                    <div>
                        <h2 class="has-text-centered is-size-5">Все заявки за
                            <select v-model="orderInterval" @change="loadOrders" class="rh-input is-primary is-small is-narrow">
                                <option value="day" selected>День</option>
                                <option value="week">Неделя</option>
                                <option value="month">Месяц</option>
                            </select>
                        </h2><b-tag>{{$store.state.orders.length}}</b-tag>
                    </div>
                    <new-order :save-url="saveUrl" :order-form="newOrderForm" ></new-order>
                    <new-driver :save-url="saveUrl"></new-driver>
                    <all-orders  v-bind:save-edit-url="saveUrl">
                    </all-orders>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import AllOrders from './components/AllOrders.vue';
    import NewOrder from './components/NewOrder.vue';
    import NewDriver from './components/NewDriver.vue';
    import suggest from './components/suggest.vue';
    import OrdersFromExcel from './components/OrdersFromExcel.vue';
    export default {
        name: 'App',
        components: {
            'all-orders': AllOrders,
            'new-order': NewOrder,
            'new-driver': NewDriver,
            suggest,
            OrdersFromExcel
        },
        data() {
            return {
                excel_file: [],
                show_create_modal: false,
                show_driver_modal: false,
                show_excel_modal: false,
                show_raworder_modal: false,
                incorrectRows : [],
                savedRows: 0,
                ignoredRows: 0,
                totalRows: 0,
                orderModalId: "newOrderModal",
                driverModalId: "newDriverModal",
                saveUrl: "/delivery/new",
                ordersUrl: "/delivery/all",
                excelSendUrl: "/delivery/parse_excel",
                customerAutocompleteUrl: "/customer-autocomplete",
                orderInterval: 'day',
            }
        },
        methods: {
            sendExcel() {
                let token = $("input[name=csrf_token]").val();
                if (this.excel_file.length === 0) {
                    this.showError({message: "Выберите файл"});
                }
                else if (!this.$store.state.customer) {
                    this.showError({message: "Выберите клиента"});
                }
                else if (this.excel_file[0].name.search(/\.xlsx?$/g) !== -1) {
                    let fd = new FormData();
                    fd.append("excel_file", this.excel_file[0]);
                    fd.append("customer",this.$store.state.customer.id);
                    $.ajax({
                        url: this.excelSendUrl, type: "POST", enctype: "multipart/form-data", contentType: false,
                        processData: false, cache: false, data: fd, success: this.respondExcel,
                        headers: {"X-CSRFToken": token}, error: this.respondErrorExcel,
                        timeout: 6000
                    });
                    this.show_excel_modal = false;
                    this.$store.commit('toggleLoading');
                }
                else
                    this.showError({message: "Файл должен быть с раширением .xls или .xlsx"});
            },
            respondExcel(data) {
                this.$store.commit('hideLoading');
                this.incorrectRows = data.incorrect_rows;
                this.savedRows = data.saved_rows;
                this.ignoredRows = data.ignored_rows;
                this.totalRows = data.total_rows;
                this.$store.commit('addOrders',data.inserted_rows);
                this.show_raworder_modal = true;
            },
            respondErrorExcel(data) {
                this.$store.commit('hideLoading');
                this.showError({message: "Ошибка сервера"});
            },
            loadOrders() {
                //this.$toast.open('загрузка...');
                let interval = this.orderInterval;
                $.ajax({url: this.ordersUrl, method: "GET", data: {interval: interval }, success: this.showResponse, error: this.showError});
                this.$store.commit('showLoading');
            },
            showResponse(data) {
                this.$store.commit('hideLoading');
                this.$store.commit('loadOrders', {orders: data.orders, orderFormDesc:  data.form_desc});
            },
            showSuccess(data) {
                this.$toast.open({message: data.message,position:'is-top',type:'is-success'});
            },
            showError(data) {
                this.$store.commit('hideLoading');
                this.$toast.open({message: data.message,position:'is-top',type:'is-danger'});
            },
        },
        created() {
            this.loadOrders();
        },
        computed: {
            newOrderForm() {
                let result = {};
                if (this.$store.state.orderFormDesc === {} || this.$store.state.orderFormDesc === null)
                    return {};
                for (let key of Object.keys(this.$store.state.orderFormDesc.types)) {
                    result[key] = {
                        type: this.$store.state.orderFormDesc.types[key],
                        label: this.$store.state.orderFormDesc.labels[key],
                        url: this.$store.state.orderFormDesc.urls[key],
                        error: '', value: this.$store.state.orderFormDesc.defaults[key],
                        required: this.$store.state.orderFormDesc.required[key]
                    };
                    if (this.$store.state.orderFormDesc.types[key] === 'select') {
                        result[key].value = {id: null, text: ''};
                        result[key].url = this.$store.state.orderFormDesc.urls[key];
                    }
                    else if (this.$store.state.orderFormDesc.types[key] === 'choice') {
                        result[key].choices = this.$store.state.orderFormDesc.choices[key];
                    }
                }
                result.customer.type = 'static';
                result.customer.value = this.$store.state.customer;
                return result;
            }
        }
    }
</script>
<style lang="scss">
    .main {
        font-family: "Roboto", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
        font-size: 10pt;
        display:flex;
        width: 100%;
        align-items: center;
        justify-content: space-around;
        flex-wrap: wrap;
    }
    .rh-col {
        flex: 1 1 auto;
    }
    .rh-input {
        border-radius: 2em;
        display: inline;
    }

    h1, h2 {
        font-weight: normal;
    }

    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        display: inline-block;
        margin: 0 10px;
    }

    a {
        color: #42b983;
    }
    .customer-select {
        float: right;
    }
</style>
