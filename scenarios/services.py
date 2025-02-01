
from .models import Execution
from .tasks import run_test_file

def run_scenario(scenario, environment=None, bank_name=None, custom_case=None):
    execution = Execution.objects.create(
        scenario_id=scenario.id,
        result='',
        status='scheduled'
    )
    run_test_file.delay(execution.pk, scenario.script_path, environment, bank_name, custom_case)
    return execution.pk
