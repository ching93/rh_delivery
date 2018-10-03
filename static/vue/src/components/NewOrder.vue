<template>
    <b-modal :active.sync="$parent.show_create_modal" has-modal-card>
        <div class="modal-card" style="width: auto">
            <header class="modal-card-head"><h5 class="modal-card-title">Новый заказ</h5></header>
            <section class="modal-card-body">
                <model-form @form-changed="orderData = $event" :saveUrl="saveUrl" :model-form.sync="form"></model-form>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-secondary" @click="$parent.show_create_modal=false">Закрыть</button>
                <button class="button is-primary" @click="saveNew">Отправить</button>
            </footer>
        </div>
    </b-modal>
</template>
<script>
import modelForm from './ModelForm.vue';
export default {
    name: 'NewOrder',
    components: {modelForm},
    data: function() {
        return {
            orderData: {},
            message: "",
            form : this.orderForm,
        }
    },
    computed: {
    },
    props: {
        modalId: String,
        saveUrl: String,
        orderForm: {type: Object, default: ()=>{}},
    },
    methods: {
        saveNew(e) {
            let data = Object.assign({action: 'create',entity: 'order'},this.orderData);
            let form = this.form;
            for (let key of Object.keys(this.form))
                this.form[key].error =  "";
            this.form = form;
            data.customer = this.$store.state.customer ? this.$store.state.customer.id: null;
            $.ajax({url: this.saveUrl, method: "GET", data: data, success: this.showResponse, error: this.showError});
        },
        showResponse(data) {
            if (data.status === 'ok') {
                this.$parent.show_create_modal = false;
                this.$toast.open("Успешно сохранено");
                //this.$emit('new-entity',data.entity);
                this.$store.commit('addOrder',data.entity);
            }
            else {
                let form = this.form;
                for (let key of Object.keys(data.errors))
                    if (key!== '')
                        this.form[key].error =  data.errors[key];
                this.form = form;
            }

        },
        showError(data) {
            this.$toast.open({message:"Ошибка!",type:'is-danger'});
        },
        plusMunites(date, minutes) {
            date.setMinutes(date.getMunites()+minutes);
            return date;
        }
    }
}
</script>
<style>

</style>