<template>
    <b-autocomplete style="min-width:100px !important" @select="$emit('change-row',$event)" v-model="text" :size="size"
                    :keep-first="keep_first" :data="rowData" field="text" :open-on-focus="true"
                    :loading="loading" @input="loadData" @click.native="loadData">
        <template slot="empty">Нет результатов</template>
    </b-autocomplete>
</template>
<script>
    export default {
        model: {
            prop: 'value',
            event: 'change-row'
        },
        props: {
            selectUrl: String,
            value: Object,
            size: {type: String, default: "is-small"}
        },
        data() {
            return {
                rowData: [this.value],
                text: '',
                loading: false,
                keep_first: false
            }
        },
        created() {
            if (this.value) {
                this.keep_first = true;
                this.text = this.value.text;
            }
        },
        methods: {
            loadData(e) {
                //let text = e.srcElement.innerText;
                //if (text.length < 2) {
                //    return false;
                //    this.selected = null;
                //}
                $.ajax({url: this.selectUrl, method: "GET", data: {q: this.text}, success: this.showData });
                this.loading = true;
            },
            showData(data) {
                this.show_suggest = true;
                if (data.results.length == 0)
                    this.rowData = [{id: null, text: 'Нет результатов'}];
                this.rowData = data.results.map((el)=>({id: parseInt(el.id), text: el.text}));
                this.loading = false;
            },
            selectRow(row) {
                if (row.id === null)
                    return;
                this.selected = row;
                this.$emit('change-row', {pk: Number.parseInt(this.selected.id), text: this.selected.text});
                //$("#"+this.name+'-list').text('');
                this.hide();
            },
            hide(e) {
                this.show_suggest = false;
            }
        },
        computed: {
            suggestedData() {

            }
        }
    }
</script>
<style >
</style>