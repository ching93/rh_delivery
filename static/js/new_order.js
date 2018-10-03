Vue.component('new-order-modal', {
    delimiters: ["[[","]]"],
    template: `
    <div class="modal fade" v-bind:id="modalId" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group" v-for="(value, key) in deliveryOrder">
                            <label for="">[[value.label ]]</label>
                            <span v-if="value.type=='textarea'"><textarea cols="40" rows="3"  v-model:value="value.value"></textarea></span>
                            <span v-else><input v-bind:type="value.type" v-model:value="value.value"></span>
                        </div>
                    </form>
                    <button class="btn btn-primary" v-on:click.prevent="saveNew">Сохранить</button>
                    <div id="msg-log"></div>
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div>
    `,
    data: function() {
        return {
            deliveryOrder: {
                driver: {label: "Имя водителя:", value: "Водила", type: "text"},
                filial: {label: "Филиал:", value: "Главный", type: "text"},
                timepoint: {label: "Время заказа:", value: new Date().toLocaleString('ru'), type: "text"},
                duration: {label: "Длительность (мин):", value: 30, type: "number"},
                remark: {label: "Примечание:", value: "", type: "textarea"},
                load_markup: {label: "Маркировка груза:", value: "вапр", type: "text"},
                address: {label: "Адрес:", value: "г. М.", type: "text"},
                loader_order: {label: "Число грузчиков:", value: 1, type: "number"},
            }
        }
    },
    computed: {

    },
    props: {
        modalId: String
    },
    methods: {
        saveNew(e) {
            let url = "/delivery/new";
            let data = {};
            for (let key of Object.keys(this.deliveryOrder)) {
                data[key] = this.deliveryOrder[key].value;
            }
            data.timepoint = this.deliveryOrder.timepoint.value.toLocaleString('ru');
            $.ajax({url: url, method: "GET", data: data, success: this.showResponse, error: this.showError});
        },
        toggleModal() {
            $("#"+modalId).modal('toggle');
        },
        showResponse(data) {
            $("#msg-log").html(data.message);
        },
        showError(data) {
            $("#msg-log").html(data.message);
        },
        plusMunites(date, minutes) {
            date.setMinutes(date.getMunites()+minutes);
            return date;
        }
    }
});