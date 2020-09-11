# -*- coding: utf-8 -*-
import copy

from rest_framework.response import Response

from backend.apis import views
from backend.apps.constants import ProjectKind
from backend.apps.configuration.mixins import TemplatePermission
from backend.apps.configuration.models import get_template_by_project_and_id
from backend.apps.configuration.showversion.serializers import GetShowVersionSLZ
from backend.apps.instance.models import VersionInstance
from backend.utils.error_codes import error_codes

from . import serializers
from .release import ReleaseDataProcessor
from .deployer import DeployController


class TemplateViewSet(views.BaseAPIViewSet, TemplatePermission):

    # TODO replace TempalteResourceView.get, but need support ResourceRequstSLZ
    def get_template_by_show_version(self, request, *args, **kwargs):
        req_data = copy.deepcopy(self.kwargs)
        req_data["project_id"] = request.project.project_id

        serializer = GetShowVersionSLZ(data=req_data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        self.can_view_template(request, validated_data["template"])
        serializer = serializers.GetFormTemplateSLZ(validated_data)

        return Response(serializer.data)


class TemplateReleaseViewSet(views.BaseAPIViewSet, TemplatePermission):
    def _request_data(self, request, project_id, template_id, show_version_id):
        request_data = request.data.copy() or {}
        show_version = {"show_version_id": show_version_id, "template_id": template_id, "project_id": project_id}
        request_data["show_version"] = show_version
        return request_data

    def _merge_path_params(self, request, **kwargs):
        request_data = request.data.copy() or {}
        request_data.update(**kwargs)
        return request_data

    def _filter_release(self, request, project_id, template_id, context):
        template = get_template_by_project_and_id(project_id, template_id)
        self.can_view_template(request, template)

        qsets = VersionInstance.objects.filter(template_id=template_id)
        namespace_id = request.query_params.get("namespace_id")
        if namespace_id:
            qsets = qsets.filter(ns_id=namespace_id)

        if context.get("latest"):
            serializer = serializers.TemplateReleaseSLZ(qsets.latest("created"))
        else:
            serializer = serializers.TemplateReleaseSLZ(qsets, many=True)
        return serializer.data

    def list_releases(self, request, project_id_or_code, template_id):
        """
        query_params = {'namespace_id': ''}
        """
        data = self._filter_release(request, request.project.project_id, template_id, context={})
        return Response(data)

    def get_latest_release(self, request, project_id_or_code, template_id):
        """
        query_params = {'namespace_id': ''}
        """
        data = self._filter_release(request, request.project.project_id, template_id, context={"latest": True})
        return Response(data)

    def create_release(self, request, project_id_or_code, template_id, show_version_id):
        """
        request.data = {
            'namespace_id': 19873,
            'namespace_variables': {'image_tag': '1.0'}
            'instance_entity': {
                'Deployment': [{'name': 'nginx-deployment', 'id': 3 # 必须传入id}]
            }
        }
        """
        if request.project.kind != ProjectKind.K8S.value:
            raise error_codes.CheckFailed(f"project_kind({request.project.kind}) is not supported")

        data = self._request_data(request, request.project.project_id, template_id, show_version_id)
        serializer = serializers.CreateTemplateReleaseSLZ(
            data=data, context={"project_kind": ProjectKind.K8S.value, "access_token": request.user.token.access_token}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        template = validated_data["template"]
        self.can_use_template(request, template)

        processor = ReleaseDataProcessor(validated_data)
        release_data = processor.release_data("create")

        controller = DeployController(user=self.request.user, project_kind=request.project.kind)
        release_id = controller.create_release(release_data)
        return Response({"release_id": release_id})

    def update_resource(self, request, project_id_or_code, template_id, release_id):
        """
        request.data = {
            'resource_name': 'Deployment',
            'name': 'nginx',
            'namespace_id': '',
            'namespace_variables': {'image_tag': '1.0'}
        }
        """
        path_params = {"project_id": request.project.project_id, "template_id": template_id, "release_id": release_id}
        serializer = serializers.UpdateTemplateReleaseSLZ(data=self._merge_path_params(request, **path_params))
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        template = validated_data["template"]
        self.can_use_template(request, template)

        processor = ReleaseDataProcessor(validated_data)
        release_data = processor.release_data("update")

        controller = DeployController(user=self.request.user, project_kind=request.project.kind)
        release_id = controller.update_release(release_data)
        return Response({"release_id": release_id})
