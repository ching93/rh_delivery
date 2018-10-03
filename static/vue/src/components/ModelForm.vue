<template>
    <section class="is-narrow">
        <b-field grouped group-multiline custom-class="is-narrow">
            <b-field v-for="(row, name) in modelForm" v-if="name!=='turnouts' && row.required" :label="row.label" :key="name" :type="row.error?'is-danger' : 'is-primary'"
                :message="row.error">
                <b-input v-if="'color,text,number,date,time,float'.includes(row.type)" :step="row.type == 'float' ? 'any' : ''"
                        v-model="row.value" :type="row.type=='float' ? 'number' : row.type" @input="dataChanged()" size="is-small" :required="row.required" ></b-input>
                <b-input v-if="'textarea'==row.type" expanded  size="is-small"
                        v-model="row.value" type="textarea" @input="dataChanged()" :required="row.required" ></b-input>
                <suggest v-if="row.type=='select'"  size="is-small" :select-url="row.url"
                         :default-value="row.value" @change-row="row.value=$event; dataChanged()"
                         :required="row.required"></suggest>
                <!--<b-datepicker v-if="row.type=='date'" v-model="row.value" @input="dataChanged()" :date-formatter="dateFormatter"
                            :date-parser="dateParser">
                </b-datepicker>
                <b-timepicker v-if="row.type=='time'" v-model="row.value" @input="dataChanged()" :time-formatter="timeFormatter"
                              :time-parser="timeParser" hour-format="24">
                </b-timepicker>-->
                <b-select v-if='row.type=="choice"' v-model="row.value" @change="dataChanged()"  size="is-small" :required="row.required">
                    <option v-for="(text,choice) in row.choices" :value="choice" :selected="choice==row.value">{{text}}</option>
                </b-select>
                <b-input v-if="row.type=='static'" type="text"  size="is-small"
                         :value="$store.state.customer ? $store.state.customer.text : 'Выберите клиента'" disabled
                         ></b-input>
                <b-taginput v-if="row.type==='list'" v-model="row.value"  size="is-small" :required="row.required">
                </b-taginput>
            </b-field>
        </b-field>
    </section>
</template>
<script>
    //import bAsyncTaginput from './b-async-taginput.vue';
    import suggest from './suggest.vue';
    export default {
        components: {
            suggest
        },
        props: {
            modelForm: {type: Object, default: {}},
            selectData: {type: Object, default: ()=>{} }
        },
        methods: {
            plusMunites(date, minutes) {
                date.setMinutes(date.getMunites()+minutes);
                return date;
            },
            dataChanged() {
                this.$emit('form-changed',this.modelData());
            },
            modelData() {
                let result = {};
                for (let key of Object.keys(this.modelForm)) {
                    if (this.modelForm[key].value === null)
                        continue;
                    else if (key === 'customer')
                        result[key] = this.$store.state.customer ? this.$store.state.customer.id : null;
                    else if (this.modelForm[key].type === 'select')
                        result[key] = this.modelForm[key].value ? this.modelForm[key].value.id : null;
                    else
                        result[key] = this.modelForm[key].value;
                }
                return result;
            },
            dateFormatter(date) {
                return [date.getDay(),date.getMonth(),date.getFullYear()].join(".");
            },
            dateParser(dateStr) {
                let items = dateStr.split(".");
                return new Date(items[2],items[1],items[0]);
            },
            timeFormatter(date) {
                return [date.getHours(), date.getMinutes()].join(":");
            },
            timeParser(timeStr) {
                let items = timeStr.split(":");
                return new Date(0,0,0,items[0],items[1]);
            },
        },
        computed: {
        }
    }
</script>
<style scoped>
</style>