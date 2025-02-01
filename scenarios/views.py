from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Scenario, Execution
from .serializers import ScenarioSerializer, ExecutionSerializer
from .services import run_scenario
import subprocess

class ScenarioViewSet(viewsets.ModelViewSet):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer

    @action(detail=False, methods=['post'], url_path='execute/(?P<pk>[^/.]+)')
    def execute(self, request, pk=None):
        scenario = self.get_object()
        
        # Extract variables from the request
        environment = request.data.get('environment', None)
        bank_name = request.data.get('bank_name', None)
        custom_case = request.data.get('custom_case', None)
        
        # Pass variables to run_scenario
        task = run_scenario(scenario, environment=environment, bank_name=bank_name, custom_case=custom_case)
        return Response({'task_id': task}, status=status.HTTP_202_ACCEPTED)

class ExecutionViewSet(viewsets.ModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer

    @action(detail=True, methods=['get'])
    def fetch_result(self, request, pk=None):
        # Проверяем, существует ли Execution с данным pk
        try:
            execution = Execution.objects.get(pk=pk)
        except Execution.DoesNotExist:
            return Response({"error": "Execution not found."}, status=status.HTTP_404_NOT_FOUND)
        
        file_path = f"/app/tmp/{pk}_execution.json"
        try:
            # Выполнение команды cat для получения содержимого файла
            output = subprocess.check_output(["cat", file_path]).decode("utf-8")
            return Response({"result": output}, status=status.HTTP_200_OK)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            return Response({"result": None, "message": "Result not yet available."}, status=status.HTTP_200_OK)

