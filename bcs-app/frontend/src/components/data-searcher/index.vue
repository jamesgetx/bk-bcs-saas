<template>
    <div class="biz-data-searcher">
        <template v-if="localScopeList.length">
            <template v-if="scopeDisabled">
                <button class="bk-button trigger-btn disabled" style="max-width: 200px;">
                    <span class="btn-text tc">{{curScope.name}}</span>
                </button>
            </template>
            <template v-else>
                <bk-selector
                    style="width: 220px; float: left; position: relative; right: -1px; z-index: 1;"
                    :placeholder="$t('请选择')"
                    :searchable="true"
                    :setting-key="'id'"
                    :display-key="'name'"
                    :selected.sync="localSearchScope"
                    :list="scopeList"
                    :search-placeholder="searchPlaceholder || $t('请选择集群')"
                    @item-selected="handleSechScope">
                </bk-selector>
            </template>
        </template>
        <div class="biz-search-input" style="width: 300px;">
            <input
                type="text"
                class="bk-form-input"
                :placeholder="placeholderRender"
                v-model="localKey"
                @keyup.enter="handleSearch" />
            <a href="javascript:void(0)" class="biz-search-btn" v-if="!localKey">
                <i class="bk-icon icon-search" style="color: #c3cdd7;"></i>
            </a>
            <a href="javascript:void(0)" class="biz-search-btn" v-else @click.stop.prevent="clearSearch">
                <i class="bk-icon icon-close-circle-shape"></i>
            </a>
        </div>
        <div class="biz-refresh-wrapper" v-if="widthRefresh">
            <bk-tooltip class="refresh" :content="$t('刷新')" :delay="500" placement="top">
                <button :class="['bk-button bk-default is-outline is-icon']" @click="handleRefresh">
                    <i class="bk-icon icon-refresh"></i>
                </button>
            </bk-tooltip>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            placeholder: {
                type: String,
                default: ''
            },
            searchPlaceholder: {
                type: String,
                default: ''
            },
            searchKey: {
                type: String,
                default: ''
            },
            searchScope: {
                type: String,
                default: ''
            },
            widthRefresh: {
                type: Boolean,
                default: true
            },
            scopeList: {
                type: Array,
                default () {
                    return []
                }
            },
            scopeDisabled: {
                type: Boolean,
                default: false
            },
            searchable: {
                type: Boolean,
                default: true
            }
        },
        data () {
            return {
                isTriggerSearch: false,
                isRefresh: false,
                localKey: this.searchKey,
                localScopeList: [],
                curScope: {
                    id: '',
                    name: this.$t('全部集群')
                },
                placeholderRender: '',
                keyword: '',
                localSearchScope: ''
            }
        },
        watch: {
            searchKey (val) {
                this.localKey = val
            },
            scopeList () {
                this.initLocalScopeList()
            },
            localKey (newVal, oldVal) {
                // 如果删除，为空时触发搜索
                if (oldVal && !newVal && !this.isRefresh) {
                    this.clearSearch()
                }
            },
            searchScope: {
                immediate: true,
                handler (val) {
                    if (val) {
                        this.localSearchScope = val
                        // this.handleSearch()
                    }
                }
            }
        },
        created () {
            this.initLocalScopeList()
            this.placeholderRender = this.placeholder || this.$t('输入关键字，按Enter搜索')
        },
        methods: {
            handleSechScope (index, data) {
                this.curScope = data
                sessionStorage['bcs-cluster'] = this.curScope.id
                this.handleSearch()
            },
            initLocalScopeList () {
                this.localScopeList = JSON.parse(JSON.stringify(this.scopeList))
                if (this.localScopeList.length) {
                    // 在初始化时，如果已经有值，选中
                    const clusterId = this.localSearchScope || sessionStorage['bcs-cluster']
                    if (clusterId) {
                        const matchItem = this.localScopeList.find(item => item.id === clusterId)
                        if (matchItem) {
                            this.curScope = matchItem
                        } else {
                            this.curScope = this.localScopeList[0]
                        }
                    } else {
                        this.curScope = this.localScopeList[0]
                    }
                    
                    sessionStorage['bcs-cluster'] = this.curScope.id
                    this.$emit('update:searchScope', this.curScope.id)
                }
            },
            handleSearch () {
                this.isTriggerSearch = true
                this.$emit('update:searchScope', this.curScope.id)
                this.$emit('update:searchKey', this.localKey)
                this.$emit('search')
                this.isRefresh = false
            },
            handleRefresh () {
                this.localKey = ''
                this.isRefresh = true
                if (this.localScopeList.length) {
                    this.curScope = this.localScopeList[0]
                }
                sessionStorage['bcs-cluster'] = this.curScope.id
                this.$emit('update:searchScope', this.curScope.id)
                this.$emit('update:searchKey', this.localKey)
                this.localSearchScope = this.curScope.id
                this.$emit('refresh')
            },
            clearSearch () {
                this.localKey = ''
                if (this.isTriggerSearch) {
                    this.handleSearch()
                    this.isTriggerSearch = false
                }
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import '../../css/mixins/clearfix.css';
    @import '../../css/mixins/ellipsis.css';
    .biz-data-searcher {
        @mixin clearfix;

        .biz-search-input {
            .bk-form-input {
                border-radius: 0 2px 2px 0;
            }
        }

        .bk-dropdown-menu {
            .dropdown-item {
                > a {
                    width: 100%;
                    cursor: pointer;
                    display: inline-block;
                    vertical-align: middle;
                    @mixin ellipsis 240px;
                }
            }
            .bk-button {
                border-radius: 2px 0 0 2px;
                border-right: none;
            }
            float: left;
        }
    }
    .trigger-btn {
        &.disabled {
            margin-right: -10px;
            cursor: default;
            background: #fafafa;
        }
    }
    .btn-text {
        width: 140px;
        text-align: left;
        display: inline-block;
        vertical-align: middle;
        @mixin ellipsis 150px;
    }
</style>
