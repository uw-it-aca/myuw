<template>
    <header>
        <div id="actions_disabled_banner" v-if="disable_actions">
            <strong>YOU ARE CURRENTLY OVERRIDING AS ANOTHER USER</strong>.
            Overriding is read-only and no actions will be saved. &nbsp;&nbsp;
            <a href="/support" style="font-weight:normal; color:#003399;">
                Back to MyUW Support tool
            </a>
        </div>

        <b-collapse id="app_search">
        </b-collapse>
        
        <b-navbar>
            <b-navbar-nav>
                <b-nav-item href="/profile/">
                    <b-icon icon="person-fill"></b-icon> {{ user.netid }}
                </b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav class="ml-auto">
                <b-nav-item v-if="user.email_error"
                    href="https://itconnect.uw.edu/connect/email/" 
                    title="UW email services">
                    <b-icon icon="exclamation-triangle"></b-icon> Email error
                </b-nav-item>
                <b-nav-item v-else
                    :href="user.email_forward_url"
                    title="Open your email in new tab">
                    <b-icon icon="envelope-fill"></b-icon> Email
                </b-nav-item>
                <b-nav-text v-b-toggle.app_search aria-label="Open search area">
                    <b-icon icon="search"></b-icon> Search
                </b-nav-text>
                <b-nav-item :href="logout_url">
                    <b-icon icon="box-arrow-right"></b-icon> Sign Out
                </b-nav-item>
            </b-navbar-nav>
        </b-navbar>
    </header>
</template>

<script>
import { mapState } from 'vuex'

export default {
    props: {
        disable_actions: {
            type: Boolean,
            default: false,
        },
        logout_url: String,
    },
    data: function() {
        return { }
    },
    computed: mapState({
        user: state => state.user
    }),
}
</script>

<style scoped>
    .navbar {
        padding: 0;
    }
</style>