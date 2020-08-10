<template>
    <b-container fluid="xl">
        <b-row>
            <b-col>
                <myuw-header :disable_actions="disable_actions"
                    :logout_url="logout_url"/>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <slot></slot>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <myuw-footer/>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import MyUWHeader from '../components/header.vue'
import MyUWFooter from '../components/footer.vue'

export default {
    components: {
        'myuw-header': MyUWHeader,
        'myuw-footer': MyUWFooter
    },
    props: {
        disable_actions: Boolean,
        logout_url: String,
    },
    data: function() {
        return { }
    }
}
</script>

<style scoped>
</style>

<style>
    html {
        font-size: 14px;
    }
</style>