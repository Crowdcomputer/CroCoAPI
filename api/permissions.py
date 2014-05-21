import logging

__author__ = 'stefano'
from rest_framework import permissions


log = logging.getLogger(__name__)

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        # log.debug("check permission")
        #if it's a task instance check ownership of the task
        if obj is None:
            # log.debug("obj is none")
            return True
        elif hasattr(obj, 'task'):
            # log.debug('is an instance')
            # log.debug("%s %s" % (obj.task.owner, request.user))
            return obj.task.owner == request.user
        #if it's a task check ownership
        elif hasattr(obj, 'owner'):
            # log.debug('is a task')
            return obj.owner == request.user
        else:
            log.debug('is smt else')
            return False


class IsExecutor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #if it's a task instance check ownership of the task
        if hasattr(obj, 'executor'):
            return obj.task.executor == request.user
        else:
            return False
