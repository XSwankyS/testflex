from rest_framework import serializers
from .models import Scenario, Execution

class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print("Serialized Scenario:", representation)  # Debug log
        return representation

class ExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print("Serialized Execution:", representation)  # Debug log
        return representation

