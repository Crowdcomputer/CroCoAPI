# Create your views here.
from datetime import datetime, timedelta
import logging
import json
from uuid import uuid4

from django.conf.urls import url, patterns, include
from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse
from rest_framework import viewsets, routers

# ViewSets define the view behavior.
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import exceptions
from api.models import Task, HumanTask, TaskInstance, Data
from api.permissions import IsOwner
from api.serializers import HumanTaskSerializer, TaskInstanceSerializer

from rest_framework_nested import routers

log = logging.getLogger(__name__)

def getTask(pk, user):
    return get_object_or_404(Task,pk=pk,owner=user)

def getInstance(pk_task,pk_instance,user):
    task = getTask(pk_task,user)
    return get_object_or_404(TaskInstance,pk=pk_instance)

def getInstanceWorker(pk_instance,worker):
    return get_object_or_404(TaskInstance,pk=pk_instance,executor=worker)


class TaskView(viewsets.ModelViewSet):
    """
    CRUD of Task
    """
    model = HumanTask
    serializer_class = HumanTaskSerializer

    def pre_save(self, obj):
        # init values
        user = self.request.user
        obj.owner = user
        if obj.uuid is None:
            obj.uuid = str(uuid4()).replace("-", "")

    # used to filter out based on the url
    def get_queryset(self):
        return HumanTask.objects.filter(owner=self.request.user)

    @action()
    def start(self, request, pk=None):
        task = getTask(pk,request.user)
        task.start()
        res={}
        res['status']=task.status
        return Response(res)

    @action()
    def stop(self, request, pk=None):
        task = getTask(pk,request.user)
        task.stop()
        res={}
        res['status']=task.status
        return Response(res)


class InstanceView(viewsets.ModelViewSet):
    """
    CRUD of taskInstance
    """
    model = TaskInstance
    serializer_class = TaskInstanceSerializer

    def list(self, request, *args, **kwargs):
        log.debug("it's the list")
        log.debug("pk %s",self.kwargs['task_pk'])
        # used for the list, otherwise the permission do not check this
        try:
            task = Task.objects.get(pk=self.kwargs['task_pk'],owner=request.user)
        except:
            raise exceptions.PermissionDenied()
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def get_queryset(self):
        return TaskInstance.objects.filter(task=self.kwargs['task_pk'])
    #
    def pre_save(self, obj):
        log.debug("pk %s", self.kwargs['task_pk'])
        obj.task = Task.objects.get(pk=self.kwargs['task_pk'])
        if obj.uuid is None or len(obj.uuid)==0:
            obj.uuid = str(uuid4()).replace("-", "")
        log.debug("obj parameters %s",obj.parameters)
        if obj.parameters is None:
            obj.parameters={}

        #     trick for the JSONFields

        input = self.request.DATA['input'] if 'input' in self.request.DATA else None
        pars= self.request.DATA['parameters'] if 'parameters' in self.request.DATA else None

        log.debug(input)
        if input is not None:
            data = obj.input_data
            if data is  None:
                data = Data()
            data.value=input
            data.save()
            obj.input_data= data


        if pars is not None:
            obj.parameters=pars
        # log.debug("%s %s"% (obj.output_data.value, obj.input_data.value))

        # if obj



    @action()
    def start(self, request, pk=None,task_pk=None):
        task_instance = getInstance(task_pk,pk, request.user)
        task_instance.start()
        res={}
        res['status']=task_instance.status
        return Response(res)

    @action()
    def stop(self, request, pk=None,task_pk=None):
        task_instance = getInstance(task_pk,pk, request.user)
        task_instance.stop()
        res={}
        res['status']=task_instance.status
        return Response(res)

    @action()
    def assign(self,request,pk=None,task_pk=None,worker=None):
        task_instance = getInstance(task_pk,pk, request.user)
        worker_id = self.request.DATA['worker'] if 'worker' in self.request.DATA else None
        if worker_id is None:
            raise exceptions.ParseError(detail="Worker ID is not specified")
        worker = User.objects.get(pk=worker_id)
        task_instance.executor=worker
        task_instance.save()
        return Response(TaskInstanceSerializer(task_instance).data)

    @action()
    def execute(self, request, pk=None,task_pk=None):
        task_instance = getInstanceWorker(pk, request.user)

        output = self.request.DATA['result'] if 'result' in self.request.DATA else None

        if output is not None:
            data = task_instance.output_data
            if data is  None:
                data = Data()
            data.value=output
            data.save()
            task_instance.output_data= data
            return Response(TaskInstanceSerializer(task_instance).data)
        else:
            raise exceptions.ParseError(detail="result is empty, what results is this then?")
# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'task', TaskView)
task_router = routers.NestedSimpleRouter(router, r'task', lookup='task')
task_router.register(r'instance', InstanceView)



# router.register(r'instance', TaskView)

# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

