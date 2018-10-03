<template>
    <b-taginput v-model="value"
                field="field" :data="workers"
                @typing="loadWorkers"
                autocomplete
                :maxtags="maxtags">
    </b-taginput>
</template>
<script>
    export default {
        props: {
            text: String,
            autocompleteUrl: String,
            maxtags: Number,
            list: {type: Object, default: [] },
            field: String
        },
        data() {
            return {
                workers: []
            };
        },
        methods: {
            loadWorkers(value) {
                $.ajax({url: this.autocompleteUrl, data:{q: value}, success: this.addWorkers});
            },
            addWorkers(data) {
                this.workers = data.results;
            },
        },
        computed: {
            value: {
                setter() {
                    this.$emit('change',this.$event);
                },
                getter() {
                    return this.list;
                }
            }
        }
    }
</script>
<style scoped>

</style>