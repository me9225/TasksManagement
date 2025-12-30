from django.db import models

# Create your models here.
ROLES=[
    (1,"מנהל"),
    (2,"עובד"),
]
STATUS_CHOICES=[
    (1,"חדש"),
    (2,"בתהליך"),
    (3,"הושלם"),
]
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True,null=False)
    employee_name = models.CharField(max_length=100,null=False)
    employee_email = models.EmailField(unique=True)
    employee_phone = models.IntegerField(unique=True)
    employee_address = models.TextField(null=False)
    employee_Team= models.ForeignKey('Team', on_delete=models.PROTECT,related_name='employees')
    employee_role=models.IntegerField(choices=ROLES)
    def __str__(self):
        return self.employee_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True,null=False)
    team_Manager_Id = models.ForeignKey(Employee,on_delete=models.PROTECT)
    def __str__(self):
        return self.team_id

class Task(models.Model):
    task_id = models.AutoField(primary_key=True,null=False)
    task_name = models.CharField(max_length=100,null=False)
    task_description = models.TextField(null=False)
    task_last_date = models.DateField(null=False)
    task_completed_date = models.DateField(null=False)
    task_status = models.IntegerField(choices=STATUS_CHOICES)
    task_team = models.ForeignKey(Team,on_delete=models.PROTECT,related_name='tasks')
    task_employee = models.ForeignKey(Employee,on_delete=models.PROTECT,related_name='MyTasks')
    def __str__(self):
        return self.task_id