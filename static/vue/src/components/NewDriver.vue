<template>
    <b-modal :active.sync="$parent.show_driver_modal" has-modal-card>
        <div class="modal-card" style="width:auto">
            <header class="modal-card-head"><h6 class="modal-card-title">Новый водитель</h6></header>
            <section class="modal-card-body">
                <model-form :model-form="form" v-on:form-changed="modelData = $event">
                </model-form>
            </section>
            <footer class="modal-card-foot">
                <button class="button" @click="$parent.show_driver_modal=false">Закрыть</button>
                <button class="button" @click="sendForm">Отправить</button>
            </footer>
        </div>
    </b-modal>
</template>
<script>
    import modelForm from './ModelForm.vue';
    export default {
        components: {'model-form': modelForm},
        props: {
            modalId: String,
            saveUrl: String,
        },
        data() {
            return {
                form: {
                    name: {label: "Имя", value: "", type: 'text', error: ""},
                    phones: {label: "Телефоны", value: [], type: 'list', error: ""},
                },
                modelData: {},
            }
        },
        methods: {
            sendForm(e) {
                let data = Object.assign({entity: 'driver'}, this.modelData);
                $.ajax({url: this.saveUrl, method: "GET", data: data, success: this.showResponse, error: this.showError});
            },
            showResponse(data) {
                //$("#msg-log").text(JSON.stringify(data));
                if (data.status === 'ok') {
                    this.$snackbar.open({message: "Успешно сохранено", type: "is-success"});
                    this.$parent.show_driver_modal = false;
                }
                else {
                    for (let key of Object.keys(data.errors))
                        if (key!== '')
                            this.form[key].error = data.errors[key];
                }
            },
            showError(data) {
                this.$snackbar.open({message: "Ошибка сервера",type:"is-danger"})
            }
        }
    }
</script>