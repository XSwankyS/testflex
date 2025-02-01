from django.db import models

class Scenario(models.Model):
    name = models.CharField(max_length=255)
    script_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Execution(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    result = models.TextField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Execution of {self.scenario.name}"
# Create your models here.
