from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from .models import *


# Create your views here.
group_login = {'group_id':'','division':'','email':'','loginstatus':False}
admin_login = {'m_id' : '','m_name':'','m_status':False}
mem_list = []
id_list = []
project_info_id = [] 

def gr_signup(req) :
    if req.method == 'POST' :
        gr = Group()
        mem = Member()

        gr.group_id = req.POST.get("group_id")
        gr.leader_id = req.POST.get('leader_id')
        gr.division = req.POST.get('div')
        gr.email = req.POST.get('email')
        gr.password = req.POST.get('password')

        group_rows = Group.objects.raw('Select * from stqa_group')
        for i in group_rows :
            if i.group_id == gr.group_id:
                return render(req,'stqa/group_signup.html', {'error':'Group Id already in use'})

        gr.save()   

        mem.mem_id = req.POST.get('leader_id')
        mem.mem_name = req.POST.get('group_leader')
        mem.grp = gr
        mem.save()     
        
        mem.mem_id = req.POST.get('id1')
        mem.mem_name = req.POST.get('mem1')
        mem.grp = gr
        mem.save()
        
        mem.mem_id = req.POST.get('id2')
        mem.mem_name = req.POST.get('mem2')
        mem.grp = gr
        mem.save()

        mem.mem_id = req.POST.get('id3')
        mem.mem_name = req.POST.get('mem3')
        mem.grp = gr
        mem.save()          

        return redirect('stqa:group_login')
    else:
        return render(req,'stqa/group_signup.html')

def gr_login(req) :

    
    if req.method == 'POST' :
         
        mem_list.clear()
        id_list.clear()

        g_id = req.POST.get('group_id'),
        pwd = req.POST.get('group_password'),        
       
        try:
            loginuser = Group.objects.raw('select * from stqa_group where group_id = %s',[g_id])[0]       # check for g_id
        except:
            return render(req,'stqa/group_login.html',{'error':'NO such group present !'})
        

        if loginuser:
            if pwd[0] == loginuser.password:
                group_login['group_id'] = loginuser.group_id
                group_login['division'] = loginuser.division
                group_login['email'] = loginuser.email
                group_login['loginstatus'] = True
                
                
                query = Member.objects.raw('select * from stqa_member where grp_id = %s',[group_login['group_id']])
                for i in query:
                    mem_list.append(i.mem_name)
                    id_list.append(i.mem_id)                # db field name    

                return redirect('stqa:group_info')
            else:
                return render(req,'stqa/group_login.html',{'error':'Invalid password'})        
        
    else :
        return render(req,'stqa/group_login.html')


    


def gr_logout(req) :

    if group_login['loginstatus'] == True:
        group_login['group_id'] = ""
        group_login['division'] = ""
        group_login['email'] = ""
        group_login['loginstatus'] = False
        
        mem_list.clear()
        id_list.clear()

        return redirect('stqa:group_login')


def manager_login(req) :

    if req.method == 'POST' :
            
        manager_id = req.POST.get('manager_id'),
        pwd = req.POST.get('manager_password'),   

        try:
            loginuser = Manager.objects.raw('select * from stqa_manager where M_id = %s',[manager_id])[0]
            #print(loginuser.m_id)
        except:
            return render(req,'stqa/manager_login.html',{'error':'NO such manager present'})
        

        if loginuser:
            if pwd[0] == loginuser.password:
                admin_login['m_id'] = loginuser.M_id
                admin_login['m_name'] = loginuser.M_name
                admin_login['status'] = True
                return redirect('stqa:manager_project_page')
            else:
                return render(req,'stqa/manager_login.html',{'error':'Invalid password'})        

    else :
        return render(req,'stqa/manager_login.html')
         
def manager_logout(req) :  

    if admin_login['m_status'] == True:
        admin_login['m_id'] = ""
        admin_login['m_name'] = ""
        admin_login['m_status'] = False
        return redirect('stqa:manager_login') 

def index(req) :
    mem_list.clear()
    id_list.clear()
    return render(req,'stqa/index.html') 

def add_projects(req) :

    if req.method == "POST":
        project = Project() 
        count = 0
        rows = Project.objects.raw('Select * from stqa_project')
        
        for i in rows:
            count+=1

        id = count + 1000
                
        project.proj_id = id
        project.grp = group_login['group_id']
        project.title = req.POST.get('project_title')
        project.domain = req.POST.get('domain')
        project.description = req.POST.get('description')
        project.status = 1
        
        project_rows = Project.objects.raw('Select * from stqa_project')
        for i in project_rows :
            if i.grp == project.grp:
                return render(req,'stqa/add_projects.html', {'error':'YOU CAN ADD ONLY ONE PROJECT'})

        
        project.save()
        return redirect('stqa:group_info') 
    else:
        return render(req,'stqa/add_projects.html')    


def group_project_page(req) :
    
    if req.method == 'POST' :       
        pass      

    elif req.method == 'GET':
        query = Project.objects.raw('select * from stqa_project where status = 1')        
        query1 = Project.objects.raw('select * from stqa_project where status = 2')
        return render(req,'stqa/group_project_page.html',{'query':query,'query1':query1})    
    
def manager_project_page(req) :
    
    if req.method == 'POST' :
        if 'group_id' in req.POST:
            #code for approval
            group_id = req.POST['group_id']

            #emaill = Group.objects.raw('select * from home_group where group_id = %s',[group_id])
            
            #Status = 2 for project approval

            with connection.cursor() as cursor:
                cursor.execute('update stqa_project set status = 2 where grp = %s',[group_id])                

                group_row = Group.objects.raw('select * from stqa_group')
                for i in group_row:
                    if i.group_id == group_id:
                        group_login['email'] = i.email

        elif 'reject_btn' in  req.POST:
            #code for rejection
            group_id = req.POST['reject_btn']

            #Status = 3 for project rejection
            with connection.cursor() as cursor:
                cursor.execute('update stqa_project set status = 3 where grp = %s',[group_id])

        elif 'info_btn' in req.POST:
            group_login['group_id'] = ""
            group_login['division'] = ""
            group_login['email'] = ""
            mem_list.clear()
            id_list.clear()
            project_info_id.clear()
            project_info_id.append(req.POST['info_btn'])
          
            print(project_info_id)
            return  redirect('stqa:project_info')
          
        elif 'info_btn1' in req.POST:
            group_login['group_id'] = ""
            group_login['division'] = ""
            group_login['email'] = ""
            mem_list.clear()
            id_list.clear()
            project_info_id.clear()
            project_info_id.append(req.POST['info_btn1'])
          
            print(project_info_id)
            return  redirect('stqa:project_info')
            
        query = Project.objects.raw('select * from stqa_project where status = 1')        
        query1 = Project.objects.raw('select * from stqa_project where status = 2')
        return render(req,'stqa/manager_project_page.html',{'query':query,'query1':query1})        
    elif req.method == 'GET':
        query = Project.objects.raw('select * from stqa_project where status = 1')        
        query1 = Project.objects.raw('select * from stqa_project where status = 2')
        return render(req,'stqa/manager_project_page.html',{'query':query,'query1':query1})    
     
def project_info(req) :

    #print(project_info_id[0])
    group_row = Group.objects.raw('select * from stqa_group')
    for i in group_row:
        if i.group_id == project_info_id[0]:
            group_login['group_id'] = i.group_id
            group_login['division'] = i.division
            group_login['email'] = i.email
    
    query = Member.objects.raw('select * from stqa_member where grp_id = %s',[group_login['group_id']])
    for i in query:
        mem_list.append(i.mem_name)
        id_list.append(i.mem_id)
   
    project_rows = Project.objects.raw('Select * from stqa_project ')
    for i in project_rows :
        if i.grp == group_login['group_id']:
            return render(req,'stqa/project_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': mem_list[0],'id1': id_list[0],'n2': mem_list[1],'id2': id_list[1],'n3': mem_list[2],'id3': id_list[2],'n4': mem_list[3],'id4': id_list[3],'email':group_login['email'],'title':i.title,'id':i.proj_id,'domain':i.domain,'description':i.description,'status':i.status})    

    return render(req,'stqa/project_info.html')

def group_info(req) :
    if group_login['loginstatus'] == True:
        if req.method == 'POST':
            with connection.cursor() as cursor:
               cursor.execute('delete from stqa_project where grp = %s',[group_login['group_id']])
            return render(req,'stqa/group_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': mem_list[0],'id1': id_list[0],'n2': mem_list[1],'id2': id_list[1],'n3': mem_list[2],'id3': id_list[2],'n4': mem_list[3],'id4': id_list[3],'email':group_login['email'],'title':"You didn't add any Project..."})    

        else :            
            project_rows = Project.objects.raw('Select * from stqa_project ')
            for i in project_rows :
               
                if i.grp == group_login['group_id']:
             
                    return render(req,'stqa/group_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': mem_list[0],'id1': id_list[0],'n2': mem_list[1],'id2': id_list[1],'n3': mem_list[2],'id3': id_list[2],'n4': mem_list[3],'id4': id_list[3],'email':group_login['email'],'title':i.title,'id':i.proj_id,'domain':i.domain,'description':i.description,'status':i.status})
            return render(req,'stqa/group_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': mem_list[0],'id1': id_list[0],'n2': mem_list[1],'id2': id_list[1],'n3': mem_list[2],'id3': id_list[2],'n4': mem_list[3],'id4': id_list[3],'email':group_login['email'],'title':"You didn't add any Project..."})    

    else :
        return render(req,'stqa/group_info.html')

