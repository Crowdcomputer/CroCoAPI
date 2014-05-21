from datetime import datetime, timedelta
from api.models import HumanTask, TaskInstance

__author__ = 'stefano'
from rest_framework import serializers


class HumanTaskSerializer(serializers.ModelSerializer):
    # pk = serializers.Field()
    #    instances = serializers.HyperlinkedIdentityField(view_name='task-instances', format='json')
    #     reward =  serializers.PrimaryKeyRelatedField()
    #     validation = serializers.PrimaryKeyRelatedField
    owner = serializers.RelatedField(source='owner.username',read_only=True)
    #    reward_type = serializers.ChoiceField(REWARDS)
    #    reward_quantity = serializers.DecimalField()

    class Meta:
        model = HumanTask
        read_only_fields = ('uuid', 'status')


class TaskInstanceSerializer(serializers.ModelSerializer):
    executor = serializers.RelatedField(source='executor.username')
    task = serializers.RelatedField(source='task.title',read_only=True)
    owner = serializers.RelatedField(source='task.owner.username',read_only=True)
    input_data=serializers.RelatedField(source='input_data.value',read_only=True)
    output_data=serializers.RelatedField(source='output_data.value',read_only=True)
    class Meta:
        model = TaskInstance
        read_only_fields = ('uuid', 'status','parameters')