# Create your views here.
import logging
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import viewsets, status








# ViewSets define the view behavior.
from rest_framework.decorators import action, api_view, permission_classes, link
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from api.exceptions import NotEnoughMoney
from api.models import Task, TaskInstance, Data, CrowdUser
from api.permissions import IsOwner
from api.serializers import  TaskInstanceSerializer, CrowdUserSerializer, TaskSerializer

from rest_framework_nested import routers

log = logging.getLogger(__name__)


def get_task(pk, user, app):
    return get_object_or_404(Task, pk=pk, owner=user, app=app)


def get_instance(pk_task, pk_instance, user, app):
    task = get_task(pk_task, user, app)
    return get_object_or_404(TaskInstance, pk=pk_instance)


def get_instance_worker(pk_instance, worker):
    return get_object_or_404(TaskInstance, pk=pk_instance, executor=worker)


@api_view(['POST'])
# @permission_classes((IsFromApp, ))
def create_user(request):
    """
    Create the user, only who has an app registered
    """
    if request.method == 'POST':
        log.debug(request.DATA)
        crowd_user = CrowdUserSerializer(data=request.DATA)
        log.debug(crowd_user.is_valid())
        if crowd_user.is_valid():
            try:
                log.debug("%s %s" % (type(crowd_user.data), crowd_user.data))
                log.debug(crowd_user.data['username'])
                if len(User.objects.all().filter(username=crowd_user.data['username'])) == 0:
                    user = User(username=crowd_user.data['username'], password=crowd_user.data['password'],
                                email=crowd_user.data['email'])
                    user.save()
                    c_user = CrowdUser(user=user)
                    c_user.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'detail': 'user exists'})
            except Exception as exc:
                log.debug(exc)
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'detail':str(exc)})
        else:
            log.debug(crowd_user.errors)
            raise exceptions.ParseError(detail=crowd_user.errors)

class TestToken(APIView):
    def get(self, request):
        ret={}
        ret['user']=request.user.username
        ret['app']=request.app.name

        return Response(ret)
    # throttle_classes = ()
    # permission_classes = ()
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    # renderer_classes = (renderers.JSONRenderer,)
    # serializer_class = AuthTokenSerializer
    # model = Token
    #
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.DATA)
    #     if serializer.is_valid():
    #         token, created = Token.objects.get_or_create(user=serializer.object['user'])
    #         return Response({'token': token.key})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(viewsets.ModelViewSet):
    """
    CRUD of Task, plus Start and Stop
    """
    model = Task
    serializer_class = TaskSerializer

    def pre_save(self, obj):
        # init values
        user = self.request.user
        obj.owner = user
        obj.app = self.request.app

    # used to filter out based on the url
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user,app=self.request.app)

    @action()
    def start(self, request, pk=None):
        task = get_task(pk, request.user, request.app)
        task.start()
        res = {}
        res['status'] = task.status
        return Response(res)

    @action()
    def stop(self, request, pk=None):
        task = get_task(pk, request.user, request.app)
        task.stop()
        res = {}
        res['status'] = task.status
        return Response(res)


class InstanceView(viewsets.ModelViewSet):
    """
    CRUD of taskInstance, plus start stop assign and execute
    """
    model = TaskInstance
    serializer_class = TaskInstanceSerializer

    def list(self, request, *args, **kwargs):
        log.debug("it's the list")
        log.debug("pk %s", self.kwargs['task_pk'])
        ''' this checks if the user owns the task, if so then the instances are displayed,
        if it's not his task then there's an exeception.
         it's a dirty way to do auth'''
        try:
            task = Task.objects.get(pk=self.kwargs['task_pk'], owner=request.user)
        except:
            raise exceptions.PermissionDenied()
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    def get_queryset(self):
        return TaskInstance.objects.filter(task=self.kwargs['task_pk'])

    #
    def pre_save(self, obj):
        obj.task = Task.objects.get(pk=self.kwargs['task_pk'])
        if self.request.user.crowduser.balance < obj.task.reward:
            raise NotEnoughMoney
        log.debug("pk %s", self.kwargs['task_pk'])

        if obj.uuid is None or len(obj.uuid) == 0:
            obj.uuid = str(uuid4()).replace("-", "")
        log.debug("obj parameters %s", obj.parameters)
        if obj.parameters is None:
            obj.parameters = {}

        #     trick for the JSONFields

        input = self.request.DATA['input'] if 'input' in self.request.DATA else None
        pars = self.request.DATA['parameters'] if 'parameters' in self.request.DATA else None

        log.debug(input)
        if input is not None:
            data = obj.input_data
            if data is None:
                data = Data()
            data.value = input
            data.save()
            obj.input_data = data

        if pars is not None:
            obj.parameters = pars
            # log.debug("%s %s"% (obj.output_data.value, obj.input_data.value))

            # if obj


    @action()
    def start(self, request, pk=None, task_pk=None):
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        task_instance.start()
        res = {}
        res['status'] = task_instance.status
        return Response(res)

    @action()
    def stop(self, request, pk=None, task_pk=None):
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        task_instance.stop()
        res = {}
        res['status'] = task_instance.status
        return Response(res)

    @action()
    def assign(self, request, pk=None, task_pk=None, worker=None):
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        worker_id = self.request.DATA['worker'] if 'worker' in self.request.DATA else None
        if worker_id is None:
            raise exceptions.ParseError(detail="Worker ID is not specified")
        worker = User.objects.get(pk=worker_id)
        task_instance.executor = worker
        task_instance.save()
        return Response(TaskInstanceSerializer(task_instance).data)

    @action()
    @permission_classes((IsOwner, ))
    # TODO: check this if only IsOwner is called
    def execute(self, request, pk=None, task_pk=None):
        task_instance = get_instance_worker(pk, request.user)

        output = self.request.DATA['result'] if 'result' in self.request.DATA else None

        if output is not None:
            data = task_instance.output_data
            if data is None:
                data = Data()
            data.value = output
            data.save()
            task_instance.output_data = data
            return Response(TaskInstanceSerializer(task_instance).data)
        else:
            raise exceptions.ParseError(detail="result is empty, what results is this then?")

    @action()
    @transaction.atomic
    def reward_give(self, request, pk=None, task_pk=None):
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        worker = task_instance.executor.crowduser
        crowdsourcer = request.user.crowduser
        crowdsourcer.balance = crowdsourcer.balance - task_instance.task.reward
        worker.balance = worker.balance + task_instance.task.reward
        resp={}
        resp["details"]="Reward of " + str(task_instance.task.reward) + " is given"
        return Response(resp)

    @action()
    @transaction.atomic
    def reward_reject(self, request, pk=None, task_pk=None):
        #TODO: implement the logic
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        resp={}
        resp["details"]="Reward of " +  str(task_instance.task.reward ) + " rejected"
        return Response(resp)

    @action()
    def quality_set(self, request, pk=None, task_pk=None):
        if 'value' not in request.DATA:
            raise exceptions.ParseError(detail="'value' not found")
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        value = int(request.DATA['value'])

        if (value>=0 and value <=100):
            task_instance.quality=value
            task_instance.save()
            resp={}
            resp["details"]="Quality set ("+value+")"
            return Response(resp)
        else:
            raise exceptions.ParseError(detail="choose a value between 0 and 100")
    @link()
    def quality_get(self, request, pk=None, task_pk=None):
        task_instance = get_instance(task_pk, pk, request.user, request.app)
        resp={}
        resp["value"]=task_instance.quality
        return Response(resp)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'task', TaskView)
task_router = routers.NestedSimpleRouter(router, r'task', lookup='task')
task_router.register(r'instance', InstanceView)

# views

# router.register(r'instance', TaskView)

# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

