<template>
    <div class="modal fade" v-bind:id="modalId" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true" v-on:keyup.enter="modalOkCallback">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">{{modalTitle}}</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
                </div>
                <div class="modal-body">
                    <slot></slot>
                    <div v-bind:id="modalId+'-msg-log'">{{message}}</div>
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Закрыть</button>
                <button type="button" class="btn btn-primary" v-bind:data-dismiss="closeOnOk ? 'modal' : ''" v-on:click="modalOkCallback">{{modalOkLabel}}</button>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        props: {
            modalTitle: {type: String, default: "Заголовок" },
            modalId: String,
            message: {type: String, default: ""},
            modalOkCallback: {type: Function, default: ()=>this.message='' },
            modalCancelCallback: {type: Function, default: ()=>'' },
            modalOkLabel: {type: String, default: "OK"},
            closeOnOk: {type: Boolean, default: false }
        },
    }
</script>