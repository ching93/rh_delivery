<template>
    <b-modal :active.sync="$parent.show_raworder_modal" has-modal-card width="90%" >
        <div class="modal-card">
            <div class="modal-card-head">
                <h6 class="modal-card-title">Отчет по загрузке</h6>
            </div>
            <div class="modal-card-body">
                <div>
                    Всего заявок: <span>{{totalRows}}</span>
                </div>
                <div>
                    Сохранено заявок: <span>{{savedRows}}</span>
                </div>
                <div>
                    Проигнорировано заявок: <span>{{ignoredRows}}</span>
                </div>
                <div>
                    Заявки с неправильными данными: <span>{{incorrectRows.length}}</span>
                </div>
                <b-table :data="incorrectRows" paginated per-page="25" >
                    <template slot-scope="props">
                        <b-table-column v-for="(value,key) in props.row" sortable :label="key" :key="key">
                            <span>{{ value }}</span>
                        </b-table-column>
                    </template>
                </b-table>
            </div>
            <div class="modal-card-foot">
                <button class="button" @click="$parent.show_raworder_modal = false">Отмена</button>
                <button class="button">Сохранить</button>
            </div>
        </div>
    </b-modal>
</template>
<script>
    export default {
        props: {
            incorrectRows: {type: Array, default: ()=>[]},
            savedRows: Number,
            ignoredRows: Number,
            totalRows: Number,
            active: {type: Boolean, default: false }
        },
        data() {
            return {

            }
        }
    }
</script>