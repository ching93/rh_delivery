<template>
    <div class="column">
        <b-table ref="orderTable"  :data="sortedOrders" paginated per-page="30" detailed detail-key="pk"
            @details-open="onDetailOpen" :default-sort="sortKey" narrowed  :opened-detailed="openedDetailed" @sort="sortKey = $event"
            >
            <template slot="header" slot-scope="props">
                <span :title="props.column.label" class="tag-wrap" >
                    <span class="tag-set">{{props.column.label}}</span>
                    {{trimStringTo(props.column.label,6)}}
                </span>
            </template>
            <template slot-scope="props">
                <b-table-column v-for="(value,key) in props.row" :key="key" :custom-key="key" :field="key"
                                :label="key == 'loading_time' ? 'Интервал' :$store.state.orderFormDesc.labels[key]"
                                sortable v-if="key!=='unloading_time' && key!=='customer' && key !== 'volume'" :custom-sort="sortOrderColumn">
                    <span class="tag-wrap">
                        <span v-if="key == 'pk'" @click="copyToBuffer(rowToString(props.row))"><b-icon pack="fa" icon="copy" type="is-primary" class="clickable" size="is-small"></b-icon></span>
                        <span v-if="$store.state.orderFormDesc.types[key]==='select' && key !== 'metro' && key !== 'customer' && value">
                            <span class="tag-set clickable" @click="copyToBuffer(value.text)" >{{value.text}}</span>
                            <span class="tag-header">{{trimString(value.text)}}</span>
                        </span>
                        <span v-if="key === 'metro'">
                            <span class="tag-set">
                                <suggest  :select-url="$store.state.orderFormDesc.urls[key]"
                                     :value="props.row[key]"  size="is-small"
                                     v-on:change-row="updateField(props.row.pk,'metro',$event.id)"></suggest>
                            </span>
                            <span class="tag-header">{{props.row[key] ? trimStringTo(props.row[key].text,5) : ''}}</span>
                            <b-icon v-if="!value" icon="edit" size="is-small" type="is-primary"></b-icon>
                        </span>
                        <span v-if="$store.state.orderFormDesc.types[key]=='choice' && value">
                            <span class="tag-set">
                                <b-select size="is-small" @input.native="updateField(props.row.pk,key,$event.target.value)" :value="value">
                                    <option v-for="(choice_val, choice_key) in $store.state.orderFormDesc.choices[key]"
                                            :value="choice_key" >{{choice_val}}</option>z
                                </b-select>
                            </span>
                            <span class="tag-header">{{trimString($store.state.orderFormDesc.choices[key][value])}}</span>
                        </span>
                        <span v-if="key == 'turnouts' && value && value.length > 0">
                            <span class="tag-set">
                                <b-tag v-for="(worker,index) in value" class="clickable" v-if="$store.state.orderFormDesc.types[key]=='select-multiple'"
                                       :key="worker.id">
                                    <span @click="copyToBuffer(worker.text)">{{worker.text}}</span>
                                </b-tag>
                            </span>
                            <span class="tag-header">{{value.length}} рабоч{{value.length==1 ? 'ий' :'их'}}</span>
                        </span>
                        <span class="tag-wrap" v-if="'text,number,textarea,float'.includes($store.state.orderFormDesc.types[key]) && key !== 'volume' && !key.includes('loading_time')" >
                            <span class="tag-set">
                                <span class="clickable" @click="copyToBuffer(value)">
                                    <a v-if="key=='address'" :href="'https://yandex.ru/maps/?mode=search&text='+value" target="_blank">
                                        <b-icon pack="fas" icon="map-marker-alt" style="margin: 0" size="is-small"></b-icon>
                                    </a>
                                    {{value}}
                                </span>
                                <b-input :value="value" :type="$store.state.orderFormDesc.types[key]" @blur="updateField(props.row.pk,key,$event.target.value)" size="is-small"></b-input>
                            </span>
                            <span class="tag-header">{{value ? trimString(value) : ''}}</span>
                        </span>
                        <span v-if="key === 'loading_time'" class="tag-wrap">
                            <span class="tag-set">{{value + ' - '+props.row['unloading_time']}}</span>
                            {{trimString(value + ' - '+props.row['unloading_time'])}}
                        </span>
                    </span>
                </b-table-column>
            </template>
            <template slot="detail" slot-scope="props">
                <b-field grouped group-multiline>
                    <b-field v-for="(value,key) of $store.state.orderFormDesc.labels" :key="key" v-if="key !== 'pk'"
                             :type="errors[key] ? 'is-danger' : 'is-primary'" size="is-small"
                        :message="errors[key]" :label="value" custom-class="is-narrow">
                        <b-input v-if="'text,number,color,textarea'.includes($store.state.orderFormDesc.types[key])" size="is-small"
                                 v-model:value="openedRow[key]" v-bind:type="$store.state.orderFormDesc.types[key]" ></b-input>
                        <b-input v-if="'float'.includes($store.state.orderFormDesc.types[key])" size="is-small"
                                 v-model:value="openedRow[key]" type="number" step="any"></b-input>
                        <b-select v-if="$store.state.orderFormDesc.types[key]==='choice'" v-model="openedRow[key]"  size="is-small">
                            <option v-for="(value,choice) in $store.state.orderFormDesc.choices[key]" :value="choice">{{value}}</option>
                        </b-select>
                        <span v-if="$store.state.orderFormDesc.types[key]==='select'" class="control">
                            <suggest :select-url="$store.state.orderFormDesc.urls[key]" :value="openedRow[key]"  size="is-small" v-on:change-row="openedRow[key]=$event"></suggest>
                        </span>
                        <b-taginput v-if="$store.state.orderFormDesc.types[key]==='select-multiple'"
                                    v-model="openedRow[key]"
                                    field="text" :data="workers"
                                    @typing="loadWorkers"
                                    autocomplete :maxtags="openedRow.loader_number"  size="is-small">
                        </b-taginput>
                    </b-field>
                </b-field>
                <b-field>
                    <button class="button is-primary" @click="saveRow">Сохранить</button>
                </b-field>
            </template>
            <template slot="empty">Нет заявок за период</template>
        </b-table>
        <textarea id="clipboard" style="visibility: hidden"></textarea>
    </div>
</template>
<script>
    import ModelForm from './ModelForm';
    import BootstrapModal from './BootstrapModal.vue';
    import suggest from './suggest.vue';
    export default {
        components: {'model-form': ModelForm, 'bootstrap-modal': BootstrapModal,suggest},
        name: 'AllOrders',
        delimiters: ["[[","]]"],
        data: function(){
            return {
                modalId: 'editModal',
                orderForm: {},
                message: '',
                editForm: null,
                errors: {},
                openedRow: null,
                openedDetailed: [],
                changedRows: {},
                sortKey: 'date',//this.$store.state.orderFormDesc.types ? {value: Object.keys(this.$store.state.orderFormDesc.types)[1], dir: 1} : null,
                workers: [],
                trimSize: 25,
            }
        },
        methods: {
            rowToString(row) {
                return [row.date, row.driver_come_time, row.driver ? row.driver.text : '', row.address, row.metro ? row.metro.text : '', row.load_markup, row.load_weight, row.remark].join("; ")
            },
            updateField(pk,key,value) {
                let data = {entity: 'order', pk, field: key, value};
                $.ajax({url: '/delivery/update', type: "GET", data: data, success: this.updateSuccess, error: this.updateError });
            },
            updateSuccess(data) {
                //this.$toast.open(JSON.stringify(data));
                this.$store.commit('updateOrder', {key: data.field, value: data.value, pk: Number.parseInt(data.pk)});
                this.$toast.open({message: "Поле сохранено", type:'is-success'});
            },
            updateError(data) {
                this.$toast.open({message: data.responseJSON.error, type:'is-danger'});
                let pk = Number.parseInt(data.pk);
                let row = this.sortedOrders.filter((row)=>(row.pk===pk))[0];
                this.$store.commit('updateOrder', {key: data.field, value: row[data.field], pk: Number.parseInt(data.pk)});
                row[field] = data.value;
            },
            /*rowClassFunc(row,index) {
                return  {'is-info':row.pk in this.changedRows};
            },*/
            copyToBuffer(text) {
                //let elem = event.target;
                let elem = $("#buffer-tag")[0];
                let oldText = elem.innerText;
                elem.innerText = text;
                let range = document.createRange();
                range.selectNode(elem);
                let sel = window.getSelection();//.Range(range);
                sel.removeAllRanges();
                sel.addRange(range);

                try {
                    let successful = document.execCommand('copy');
                    let msg = successful ? text : 'unsuccessful';
                    this.$toast.open("Скопировано " + msg);
                } catch(err) {
                    this.$toast.open('Oops, unable to copy');
                }

                window.getSelection().removeAllRanges();
                elem.innerText = oldText;
            },
            setSorted(key) {
                if (this.sortKey.value == key)
                    this.sortKey = {value: key, dir: -this.sortKey.dir};
                else
                    this.sortKey = {value: key, dir: 1};
            },
            trimString(st) {
                return st.length > this.$store.state.charCount ? st.slice(0,this.$store.state.charCount) + ".." : st;
            },
            trimStringTo(st,num) {
                if (typeof(st) == 'string')
                    return st.length > num ? st.slice(0,num) + ".." : st;
                else
                    return st;
            },
            saveRow() {
                let data = {action: 'edit', entity: 'order'};
                //data.pk = this.editForm.pk;
                for (let key of Object.keys(this.openedRow)) {
                    let value = this.openedRow[key];
                    if (key == 'turnouts') {
                        let list = [];
                        let old = [];
                        for (let item of value)
                            if (item.pk)
                                old.push(item.pk);
                            else
                                list.push(item.id);
                        data['new_workers'] = list;//.join(",");
                        data['turnouts_new'] = old;//.join(",");
                    }
                    else if (typeof(value) == 'object') {
                        data[key] = value ? (value.pk ? value.pk : value.id) : null;
                    }
                    else
                        data[key] = value;

                }
                $.ajax({url: this.saveEditUrl, data, success: this.showResult, error: this.showError });
            },
            onDetailOpen(row,index) {
                this.openedDetailed = [row.pk ];
                this.openedRow = Object.assign({},row);
            },
            showResult(data) {
                if (data.status == 'ok') {
                    let pk = parseInt(data.entity.pk);
                    let order = this.$store.state.orders.filter((r)=>r.pk===pk)[0];
                    let index = this.$store.state.orders.indexOf(order);
                    this.$store.commit('replaceOrder',index,data.entity);
                    this.editForm = null;
                    this.errors = {};
                    this.showSuccess("Изменения сохранены");
                }
                else {
                    this.errors = data.errors;
                }
            },
            loadWorkers(value) {
                $.ajax({url: this.$store.state.orderFormDesc.urls.turnouts, data:{q: value}, success: this.addWorkers});
            },
            addWorkers(data) {
                this.workers = data.results;
            },
            showWarning(message) {
                this.$toast.open({message: message,type:'is-warning'});
            },
            showSuccess(message) {
                this.$toast.open({message: message,type:'is-success'});
            },
            showError() {
                this.$toast.open({message:"Ошибка сервера",type:'is-danger'});
            },
            setOrderForm(order) {
                let result = {};
                for (let key of Object.keys(order))
                    if (key === 'pk')
                        result[key] = {value: order[key]};
                    else
                        result[key] = {label: this.$store.state.orderFormDesc.labels[key],
                            type: this.$store.state.orderFormDesc.types[key],
                            value: order[key],
                            url: this.$store.state.orderFormDesc.urls[key] ? this.$store.state.orderFormDesc.urls[key] : ''};
                this.orderForm = result;
                this.openModal();
            },
            showEdit(key,pk) {
                let result = false;
                if (this.editForm!==null)
                    if (this.editForm.order.pk===pk && this.editForm.key ===key)
                        result = true;
                return result;
            },
            sortOrderColumn(a,b,asc) {
                let dir = asc ? -1 : 1;
                if (this.$store.state.orderFormDesc[this.sortKey] === 'select')
                    if (a[this.sortKey] && b[this.sortKey])
                        return a[this.sortKey].text.localeCompare(b[this.sortKey].text)*dir;
                    else if (a[this.sortKey])
                        return dir;
                    else
                        return -dir;
                else if (this.$store.state.orderFormDesc[this.sortKey] === 'text')
                    return a[this.sortKey].localeCompare(b[this.sortKey])*dir;
                else
                    return a[this.sortKey] > b[this.sortKey] ? dir : -dir;
            }
        },
        props: {
            formUrls: {type: Object, default: ()=>{} },
            saveEditUrl: String
        },
        computed: {
            headers() {
                let result = [];
                for (let key of Object.keys(this.$store.state.orderFormDesc.labels)) {
                    let width = "number,time".includes(this.$store.state.orderFormDesc.types[key]) ? '10' : '';
                    result.push(
                        {
                            field: key,
                            label: this.trimString(this.$store.state.orderFormDesc.labels[key]),
                            width: width,
                            meta: this.$store.state.orderFormDesc.labels[key],
                            sortable: true,
                        });
                }
                return result;
            },
            resultClass() {
                if (this.editForm)
                    if (this.editForm.result==='success')
                        return {success: true};
                    else if (this.editForm.result==='error')
                        return {error: true};
                return {changed: true};
            },
            sortedOrders() {
                let res = [];
                if (this.$store.state.customer !== null) {
                    res =  this.$store.state.orders.filter((o) => (o.customer.pk == this.$store.state.customer.id));
                }
                else {
                    res = this.$store.state.orders;
                }
                return res;
            },
        }
    }
</script>
<style lang="scss" >
    .is-info {
        background: hsl(171, 100%, 41%);
        color: white;
    }
    .tag-set {
        display: flex;
        flex-direction: column;
        visibility: hidden;
        position: absolute;
        background-color: white;
        border-radius: 3px;
        z-index: 2;
        //border: 1px solid grey;
        padding: 3px;
    }
    .tag-header {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        word-wrap: normal;
        max-height: 10px !important;
    }
    .tag-wrap:hover .tag-set {
        visibility: visible;
    }
    .tag-header {
        text-decoration: dashed;
    }
    td, th {
        min-width: 10px;
    }
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
        opacity: 0;
    }
    .sortHeader {
        border: 1px dashed deepskyblue;
    }
    .sortHeaderPos {
        border: 1px dashed deepskyblue;
    }
    .sortHeaderNeg {
        border: 1px dashed deepskyblue;
    }
    .clickable {
        cursor: pointer;
    }
</style>