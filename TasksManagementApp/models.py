from django.db import models
from django.contrib.auth.models import AbstractUser
from sympy import false

# Create your models here.
STATUS_CHOICES=[
    (1,"חדש"),
    (2,"בתהליך"),
    (3,"הושלם"),
]
class Employee(AbstractUser):
    ROLES=[
        (1,"מנהל"),
        (2,"עובד"),
    ]
    employee_Team= models.ForeignKey('Team', on_delete=models.PROTECT,related_name='employees',null=True,blank=True)
    employee_role=models.PositiveSmallIntegerField(choices=ROLES,null=False,default=2)
    def __str__(self):
        return self.username

class Team(models.Model):
    team_id = models.AutoField(primary_key=True,null=False)
    team_Manager_Id = models.ForeignKey('Employee',on_delete=models.PROTECT, related_name='teams',null=False)
    def __str__(self):
        return str(self.team_id)

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