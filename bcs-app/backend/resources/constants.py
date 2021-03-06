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
from backend.utils.basic import ChoicesEnum


class WorkloadTypes(ChoicesEnum):
    Deployment = "Deployment"
    StatefulSet = "StatefulSet"
    DaemonSet = "DaemonSet"
    Job = "Job"
    GameStatefulSet = "GameStatefulSet"
    GameDeployment = "GameDeployment"

    _choices_labels = (
        (Deployment, "Deployment"),
        (StatefulSet, "StatefulSet"),
        (DaemonSet, "DaemonSet"),
        (Job, "Job"),
        (GameStatefulSet, "GameStatefulSet"),
        (GameDeployment, "GameDeployment"),
    )


class K8sResourceKinds(ChoicesEnum):
    Deployment = "Deployment"
    StatefulSet = "StatefulSet"
    DaemonSet = "DaemonSet"
    Job = "Job"
    ConfigMap = "ConfigMap"
    Ingress = "Ingress"
    Secret = "Secret"
    Service = "Service"
    Endpoints = "Endpoints"
    Namespace = "Namespace"
    Node = "Node"
    Pod = "Pod"

    _choices_labels = (
        (Deployment, "Deployment"),
        (StatefulSet, "StatefulSet"),
        (DaemonSet, "DaemonSet"),
        (Job, "Job"),
        (ConfigMap, "ConfigMap"),
        (Ingress, "Ingress"),
        (Secret, "Secret"),
        (Service, "service"),
        (Endpoints, "Endpoints"),
        (Namespace, "Namespace"),
        (Pod, "Pod"),
    )


class K8sServiceTypes(ChoicesEnum):
    ClusterIP = "ClusterIP"
    NodePort = "NodePort"
    LoadBalancer = "LoadBalancer"

    _choices_labels = ((ClusterIP, "ClusterIP"), (NodePort, "NodePort"), (LoadBalancer, "LoadBalancer"))


class PatchType(ChoicesEnum):
    JSON_PATCH_JSON = "application/json-patch+json"
    MERGE_PATCH_JSON = "application/merge-patch+json"
    STRATEGIC_MERGE_PATCH_JSON = "application/strategic-merge-patch+json"
    APPLY_PATCH_YAML = "application/apply-patch+yaml"

    _choices_labels = (
        (JSON_PATCH_JSON, "application/json-patch+json"),
        (MERGE_PATCH_JSON, "application/merge-patch+json"),
        (STRATEGIC_MERGE_PATCH_JSON, "application/strategic-merge-patch+json"),
        (APPLY_PATCH_YAML, "application/apply-patch+yaml"),
    )
