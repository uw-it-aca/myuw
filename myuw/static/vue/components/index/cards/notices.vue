<template>
    <uw-card :loaded="isReady">
        <template #card-heading>
            Notices
        </template>
        <template #card-body>
            <p v-if="notices.length == 0">
                You do not have any notices at this time.
            </p>
            <ul v-else>
                <li v-for="notice in notices" :key="notice.id_hash">
                    <div class="notice-container">
                         <span class="notice-title">
                            <span class="notice-critical" v-if="notice.is_critical">
                                Critical:
                            </span>
                            <b-link v-b-toggle="notice.id_hash"
                                class="p-0 notice-link" variant="link"
                                v-html="notice.notice_title">
                            </b-link>
                            <span v-if="!notice.is_read" class="notice-new">
                                New
                            </span>
                        </span>
                    </div>
                    <b-collapse v-on:shown="onShowNotice(notice)"
                                :id="notice.id_hash" tabindex="0">
                        <div class="notice-body" v-html="notice.notice_body"></div>
                    </b-collapse>
                </li>
            </ul>
        </template>
    </uw-card>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import Card from '../../../containers/card.vue'

export default {
    components: {
        'uw-card': Card,
    },
    data: function() {
        return {
            loading: true,
        }
    },
    computed: {
        ...mapState({
            notices: state => {
                return state.notices.value.filter(
                    notice => notice.is_critical ||
                            notice.category.includes("Legal") ||
                            notice.location_tags.includes('notices_date_sort') ||
                            notice.location_tags.includes('notice_banner')
                ).sort((n1, n2) => {
                    if (n1.is_critical !== n2.is_critical) return n2.is_critical;
                    return n2.date - n1.date;
                });
            }
        }),
        ...mapGetters('notices', {
            isReady: 'isReady',
        }),
    },
    created() {
        this.$store.dispatch('notices/fetch');
    },
    methods: {
        onShowNotice(notice) {
            if (!notice.is_read) {
                this.$store.dispatch('notices/setRead', notice);
            }
        },
    }
}
</script>

<style lang="scss" scoped>

</style>