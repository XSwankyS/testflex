import os
from .models import Execution, Scenario
from test_runner.celery import app
from pathlib import Path
import subprocess

@app.task
def run_test_file(execution_id, script_path, environment=None, bank_name=None, custom_case=None):
    # Изменён путь сохранения файла отчёта на /app/tmp/
    json_result_path = f"/app/tmp/{execution_id}_execution.json"
    
    # Debugging: write received variables to /tmp/command.file for verification
    with open('/tmp/command.file', 'w') as debug_file:
        debug_file.write(f"Received variables:\n")
        debug_file.write(f"environment: {environment}\n")
        debug_file.write(f"bank_name: {bank_name}\n")
        debug_file.write(f"custom_case: {custom_case}\n")
    
    # Construct the pytest command with variables right after pytest
    command = ['pytest']
    
    if custom_case:
        command.extend(custom_case.split())  # Split to handle cases like "-w -s"
    if environment:
        command.append(f'--env={environment}')
    if bank_name:
        command.append(f'--bname={bank_name}')
    
    # Add the script path and json-report arguments
    command.extend([script_path, '--json-report', f'--json-report-file={json_result_path}'])
    
    # Append the final constructed command to /tmp/command.file
    with open('/tmp/command.file', 'a') as debug_file:
        debug_file.write("\nConstructed command:\n")
        debug_file.write(' '.join(command))
    
    env = os.environ.copy()    
    
    # Run the process
    process = subprocess.run(command)
    
    json_result_file = Path(json_result_path)
    
    # Update the execution result in the database
    Execution.objects.filter(
        id=execution_id,
    ).update(
        status='completed' if process.returncode == 0 else 'failed',
        result=json_result_file.read_text()
    )

