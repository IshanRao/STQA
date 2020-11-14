from django.db import models

# Create your models here.
class Group(models.Model) :
    group_id = models.CharField(max_length=10,primary_key=True)
    leader_id = models.ForeignKey('Member', on_delete=models.CASCADE)
    division = models.CharField(max_length=1)
    email = models.EmailField()
    password = models.CharField(max_length=50)
      

class Member(models.Model) :
    mem_id = models.CharField(max_length=10,primary_key=True)
    mem_name = models.CharField(max_length=30)
    grp = models.CharField(max_length=10)

class Manager(models.Model) :
    M_id = models.CharField(max_length=10,primary_key=True)
    M_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)    
    
class Project(models.Model) :

    proj_id = models.CharField(max_length=10,primary_key=True)
    grp = models.CharField(max_length = 10)
    title = models.CharField(max_length=50)
    description = models.TextField()
    domain = models.CharField(max_length=50)
    status = models.IntegerField(default=0)    