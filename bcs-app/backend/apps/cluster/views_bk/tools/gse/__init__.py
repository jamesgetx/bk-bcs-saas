# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
# Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
from backend.components import gse


class GSEClient:

    @classmethod
    def get_agent_status(cls, request, ip_list):
        hosts = []
        for info in ip_list:
            plat_info = info.get('bk_cloud_id') or []
            plat_id = plat_info[0]['id'] if plat_info else 0
            hosts.extend([
                {'plat_id': plat_id, 'bk_cloud_id': plat_id, 'ip': ip}
                for ip in info.get('inner_ip', '').split(',')
            ])
        return gse.get_agent_status(request.user.username, hosts)
