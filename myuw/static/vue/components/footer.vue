<template>
    <footer>
        <b-list-group horizontal>
            <b-list-group-item :href="'mailto:help@uw.edu?subject=MyUW%20Comment,%20Request,%20Suggestion&body=Hello,%0A%0A%3CInclude%20your%20comment%20or%20question%20about%20MyUW%20here%3e%0A%0A%0A%0ANetID%3A%20$' + user.netid">
                <b-icon icon="envelope-fill"></b-icon> Contact
            </b-list-group-item>
            <b-list-group-item href="https://itconnect.uw.edu/learn/tools/myuw-help-center/">
                MyUW Help
            </b-list-group-item>
            <b-list-group-item>Sign Out</b-list-group-item>
            <b-list-group-item >Terms</b-list-group-item>
            <b-list-group-item >Privacy</b-list-group-item>
        </b-list-group>
        <span>&copy; {{(new Date()).getFullYear()}} University of Washington</span>
    </footer>
</template>

<script>
import { mapState } from 'vuex'

export default {
    data: function() {
        return { }
    },
    computed: mapState({
        user: state => state.user
    }),
}
</script>

<style scoped>
</style>