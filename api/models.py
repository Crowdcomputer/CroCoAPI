from datetime import datetime, timedelta
import json
from django.contrib.auth.models import User
from django.db import models
from django.dispatch.dispatcher import receiver
from jsonfield import JSONField
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class Data(models.Model):
    value = JSONField()

    def __unicode__(self):
        return str(self.id)

# REWARDS = (('CCM', 'CrowdComputer'), ('USD', 'Dollars'), ('EUR', 'Euro'), ('COF', 'Coffies'),)
# STRATEGIES = (('ALL','Pay all'),('NONE','Pay None'),('VALID','Pay Valid'),('BEST','Pay Best'))
# class Reward(models.Model):
# #    description = models.CharField(max_length=100, default='')
#     quantity = models.DecimalField(decimal_places=2, max_digits=8, default=Decimal('0.0'), blank=True, null=True)
#     reward_type = models.CharField(max_length=3, choices=REWARDS, default='CCM')
#     strategy = models.CharField(max_length=10, choices=STRATEGIES, default='ALL')

STATUS_CHOISES = (('PR', 'In process'), ('ST', 'Stopped'), ('FN', 'Finished'), ('DL', 'Deleted'),)


class Task(models.Model):
    owner = models.ForeignKey(User)
    # process = models.ForeignKey(Process)
    title = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=1000, default='')
    date_created = models.TimeField(auto_now_add=True, auto_now=False)
    date_deadline = models.DateTimeField(default=lambda: (datetime.now() + timedelta(days=7)), auto_now_add=False)
    # parameters = jsonfield.JSONField(blank=True)
    # objects = InheritanceManager()
    status = models.CharField(max_length=2, choices=STATUS_CHOISES, default='ST', blank=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + str(self.title)

    def start(self):
        self.status = "PR"
        self.save()

    def stop(self):
        self.status = "ST"
        self.save()

    def finish(self):
        self.status = 'FN'
        self.save()

    def delete(self):
        self.status = 'DL'
        self.save()


        # @property
        # def is_inprocess(self):
        #     return self.status == 'PR'
        # @property
        # def is_stopped(self):
        #     return self.status == 'ST'
        # @property
        # def is_finished(self):
        #     return self.status == 'FN'
        # @property
        # def is_deleted(self):
        #     return self.status == 'DL'
        # @property
        # def is_expired(self):
        #     return (self.date_deadline < datetime.utcnow().replace(tzinfo=utc))
        #
        #
        # @property
        # def instances_given(self):
        #     return self.taskinstance_set.filter(status='FN').count()
        # @property
        # def instances_available(self):
        #     return self.taskinstance_set.filter(status='ST').count()
        # @property
        # def instances_running(self):
        #     valid= self.taskinstance_set.filter(status='VL').count()
        #     progress = self.taskinstance_set.filter(status='PR').count()
        #     return valid+progress
        # @property
        # def instances_amount(self):
        #     return self.taskinstance_set.all().count()
        #
        # def finish(self):
        #     self.status = 'FN'
        #     self.save()
        #
        #
        # def delete(self):
        #     self.status = 'DL'
        #     self.save()


# PLATFORMS = (('CC', 'CrowdComputer'), ('MT', 'Amazon Mechanical Turk'),)
class HumanTask(Task):
    # is_unique = models.BooleanField(default=True)
    # number_of_instances = models.IntegerField(default=1)
    uuid = models.CharField(max_length=36, default='')
    page_url = models.URLField(max_length=400, default='', null=True, blank=True)
    # platform = models.CharField(max_length=2, choices=PLATFORMS, default='CC')
    # validation = models.CharField(max_length=400, default=None,null=True, blank=True)
    # reward = models.OneToOneField(Reward, null=True, blank=True)


STATUS_CHOICES = (('ST', 'Stopped'), ('PR', 'Process'), ('FN', 'Finished'), ('VL', 'Validation'))


class TaskInstance(models.Model):
    # executor
    executor = models.ForeignKey(User, null=True, blank=True)
    # mto1: many Responses generated for one task
    task = models.ForeignKey(Task)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='ST')
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_started = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    date_finished = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    input_data = models.ForeignKey(Data, null=True, blank=True, related_name="input_data")
    output_data = models.ForeignKey(Data, null=True, blank=True, related_name="output_data")
    uuid = models.CharField(max_length=36, default='')
    parameters = JSONField(blank=True,null=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] '

    def start(self):
        self.status = "PR"
        self.save()

    def stop(self):
        self.status = "ST"
        self.save()

    def finish(self):
        self.status = 'FN'
        self.save()

    def delete(self):
        self.status = 'DL'
        self.save()
    # validation = models.OneToOneField(Process, null=True, blank=True)

    # def __unicode__(self):
    #     return str(self.id)
    #
    # @property
    # def is_inprocess(self):
    #     return self.status == 'PR'
    #
    # @property
    # def is_stopped(self):
    #     return self.status == 'ST'
    #
    # @property
    # def is_finished(self):
    #     return self.status == 'FN'
    #
    # @property
    # def is_deleted(self):
    #     return self.status == 'DL'
    #
    # @property
    # def is_validation(self):
    #     return self.status == 'VL'
    #
    # def start(self):
    #     self.status = 'PR'
    #     self.date_started = datetime.now()
    #     self.save()
    #
    # def finish(self):
    #     self.status = 'FN'
    #     self.date_finished = datetime.now()
    #     self.save()
    #
    # def validation_status(self):
    #     self.status = 'VL'
    #     self.save()


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)