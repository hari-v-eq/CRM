import email
from email import message, message_from_binary_file
import imp
from turtle import title
from urllib import request
from winsound import MessageBeep
from django.shortcuts import render, redirect

from CEO.forms import EventForm
from .models import *
from datetime import datetime, timedelta, date
from django.views import generic
import calendar
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .utils import Calendar
from .forms import EventForm
import json, urllib
from django.http import JsonResponse

# Create your views here.
def home(request):
     if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        tid=Task.objects.all()
        nmsg_id=Message.objects.all()
        event_all=Event.objects.all()
        if uid.role =="CEO" or uid.role =="ceo":
            cid=CEO.objects.get(user_id=uid)
            mcount=Manager.objects.all().count()
            ecount=Employee.objects.all().count()
            tcount=Task.objects.all().count()
            
            # msgcount=Message.objects.all().count()
            msgcount=Message.objects.filter(status="Pending").count()
            return render( request, 'CEO/home.html',{'uid':uid,'tid':tid, 'cid':cid,'mcount':mcount,'ecount':ecount,'tcount':tcount,'msgcount':msgcount,'nmsg_id':nmsg_id,'event_all':event_all})  
        else:
            return render(request,"CEO/login.html")  

def mhome(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])  
        tid=Task.objects.all()     
        mid=Manager.objects.get(user_id=uid)
        name=mid.firstname
        nmsg_id=Message.objects.filter(firstname=name)
        if uid.role =="Manager" or uid.role =="manager":
            mcount=Manager.objects.all().count()
            ecount=Employee.objects.all().count()
            tcount=Task.objects.all().count()
            msgcount=Message.objects.filter(status="Pending").count()
          
            return render( request, 'CEO/mhome.html',{'uid':uid, 'mid':mid,'mcount':mcount,'ecount':ecount,'tcount':tcount,'nmsg_id':nmsg_id,'tid':tid,'msgcount':msgcount})
        else:
            return render(request,"CEO/login.html")  

def ehome(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])  
        tid=Task.objects.all()     
        eid=Employee.objects.get(user_id=uid)
        name=eid.firstname
        nmsg_id=Message.objects.filter(firstname=name)
        if uid.role =="Employee" or uid.role =="employee":
            mcount=Manager.objects.all().count()
            ecount=Employee.objects.all().count()
            tcount=Task.objects.all().count()
            msgcount=Message.objects.filter(status="Pending").count()
          
            return render( request, 'CEO/ehome.html',{'uid':uid, 'eid':eid,'mcount':mcount,'ecount':ecount,'tcount':tcount,'nmsg_id':nmsg_id,'tid':tid,'msgcount':msgcount})
        else:
            return render(request,"CEO/login.html")  

def login(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])
        tid=Task.objects.all()
        
        if uid.role =="CEO" or uid.role == "ceo":
            cid=CEO.objects.get(user_id=uid)  
            mcount=Manager.objects.all().count()
            ecount=Employee.objects.all().count()
            tcount=Task.objects.all().count()                        
            return render( request, 'CEO/home.html',{'uid':uid, 'cid':cid,'tid':tid,'mcount':mcount,'ecount':ecount,'tcount':tcount})
        elif uid.role=="Manager" or uid.role=="manager":
            mid=Manager.objects.get(user_id=uid)           
            return render( request, 'CEO/mhome.html',{'uid':uid, 'mid':mid})    
        elif uid.role=="Employee" or uid.role=="employee":
            eid=Employee.objects.get(user_id=uid)          
            return render( request, 'CEO/ehome.html',{'uid':uid, 'eid':eid})       
    if request.POST:        
        pemail=request.POST['email']
        ppassword=request.POST['password']

    try:
        uid=User.objects.get(email=pemail,password=ppassword)
        if uid.password==ppassword:
            print("+++",uid.role)
            if uid.role=="CEO" or uid.role=="ceo":
                print("CEO")
                cid=CEO.objects.get(user_id=uid)                   
                request.session['email']=uid.email
                return render(request,"CEO/home.html", {'uid':uid, 'cid':cid})
            
            elif uid.role=="Manager" or uid.role=="manager":   
                print("Manager")                 
                mid=Manager.objects.get(user_id=uid)
                request.session['email']=uid.email
                return render(request,"CEO/mhome.html", {'uid':uid, 'mid':mid})

            elif uid.role=="Employee" or uid.role=="employee": 
                print("Employee")                 
                eid=Employee.objects.get(user_id=uid)  
                request.session['email']=uid.email
                return render(request,"CEO/ehome.html", {'uid':uid, 'eid':eid})
            
        else:
            e_msg="Invalid password"
            return render(request,"CEO/login.html",{'e_msg':e_msg})
    except:  
        return render(request,"CEO/login.html")
    else: 
        return render(request,"CEO/login.html")

def register(request):

    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        role=request.POST['role']
        uid=User.objects.create(email=email,role=role,password=password)  
        uid.save()  
        s_msg="Account Created Successfully"
        return render (request, "CEO/login.html",{'s_msg':s_msg})
    else:
        return render (request, "CEO/register.html")

def logout(request):
    if "email" in request.session:
        del request.session['email']
        s_msg="Successfully Logged out"
        return render(request,"CEO/login.html",{'s_msg':s_msg})       
    else:
        return render(request,"CEO/login.html")

def c_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session ['email'] )
        if request.POST:
            currentpassword=request.POST['currentpassword']
            newpassword=request.POST['newpassword']

            if uid.password==currentpassword:
                uid.password=newpassword
                uid.save()    #update
                u_msg="Password updated Successfully"
                return render(request,"CEO/c_profile.html",{'uid':uid,'u_msg':u_msg}) 
        
        if uid.role=='CEO' or 'ceo':
            cid = CEO.objects.get(user_id = uid)
            return render(request,"CEO/c_profile.html",{'uid':uid, 'cid':cid})
          
        else:
            return render(request,"CEO/home.html",{'uid':uid,'cid':cid})      

def m_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session ['email'] )
        if request.POST:
            currentpassword=request.POST['currentpassword']
            newpassword=request.POST['newpassword']

            if uid.password==currentpassword:
                uid.password=newpassword
                uid.save()    #update
                u_msg="Password updated Successfully"
                return render(request,"CEO/m_profile.html",{'uid':uid,'u_msg':u_msg}) 
        
        if uid.role=="Manager" or uid.role=="manager":
            mid = Manager.objects.get(user_id = uid)
            return render(request,"CEO/m_profile.html",{'uid':uid, 'mid':mid})
          
        else:
            return render(request,"CEO/mhome.html",{'uid':uid,'mid':mid})      

def e_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email= request.session ['email'] )
        if request.POST:
            currentpassword=request.POST['currentpassword']
            newpassword=request.POST['newpassword']

            if uid.password==currentpassword:
                uid.password=newpassword
                uid.save()    #update
                u_msg="Password updated Successfully"
                return render(request,"CEO/e_profile.html",{'uid':uid,'u_msg':u_msg}) 
        
        if uid.role=="Employee" or uid.role=="employee": 
            eid = Employee.objects.get(user_id = uid)
            return render(request,"CEO/e_profile.html",{'uid':uid, 'eid':eid})
          
        else:
            return render(request,"CEO/ehome.html",{'uid':uid,'eid':eid})      

def edit(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)      
        mid=Manager.objects.get(firstname=id)
        
        if request.POST:
            
            mid.lastname=request.POST['lastname']
            mid.contact=request.POST['contact']
            mid.salary=request.POST['salary']
          
            mid.job_profile=request.POST['job_profile']
            mid.address=request.POST['address']
            mid.save()
            u_msg="Profile updated Successfully"
            return render(request, 'CEO/edit.html',{"mid":mid,"uid":uid,'cid':cid,'u_msg':u_msg})
        else:
            return render(request, 'CEO/edit.html',{"mid":mid,"uid":uid,'cid':cid})

def eedit(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)      
        eid=Employee.objects.get(firstname=id)
        
        if request.POST:
            
            eid.lastname=request.POST['lastname']
            eid.contact=request.POST['contact']
            eid.salary=request.POST['salary']
            eid.job_profile=request.POST['job_profile']
            eid.address=request.POST['address']
            eid.save()
            u_msg="Profile updated Successfully"
            return render(request, 'CEO/eedit.html',{"eid":eid,"uid":uid,'cid':cid,'u_msg':u_msg})
        else:
            return render(request, 'CEO/eedit.html',{"eid":eid,"uid":uid})

def add_manager(request):    
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)
        if request.POST:
            email=request.POST['email']
            password=request.POST['password']
            role=request.POST['role']
            uid=User.objects.create(email=email,role=role,password=password)  
            uid.save()  
            mid=Manager.objects.create(
                   user_id=uid,                
                firstname=request.POST['firstname'],               
                lastname=request.POST['lastname'],
                contact=request.POST['contact'],
                birthdate=request.POST['birthdate'],
                joiningdate=request.POST['joiningdate'],
                salary=request.POST['salary'],
                job_profile=request.POST['job_profile'],
                marital_status=request.POST['marital_status'],
                address=request.POST['address'],
                gender=request.POST['gender'],
                id_proof=request.FILES['id_proof'],
                profile_pic=request.FILES['profile_pic'],
                
                )
            

            if mid:            
                m_all= Manager.objects.all()
                print("+++++++++++++++++",m_all)
                return render(request,"CEO/all_manager.html",{"m_all":m_all,"uid":uid,'cid':cid})
        else:
            return render(request,"CEO/add_manager.html",{"uid":uid})    
    else:
        return redirect('login')


def json(request):


    message=list(Event.objects.all().values())

    return JsonResponse(message,safe=False)




def all_manager(request):
    
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        cid=CEO.objects.get(user_id=uid)
        mid = Manager.objects.all()

        
        if uid.role=='CEO' or "ceo":
            
            return render(request,"CEO/all_manager.html",{"mid":mid,"uid":uid,'cid':cid}) 

        elif uid.role=="Manager" or "manager":
            
            return render(request,"CEO/all_manager.html",{"mid":mid,"uid":uid})  

def all_employee(request):
    if 'email' in request.session:
        uid=User.objects.get(email=request.session['email'])
        cid=CEO.objects.get(user_id=uid)
        eid=Employee.objects.all()

        if uid.role=='Employee' or "employee":
            
            return render(request,"CEO/all_employee.html",{"eid":eid,"uid":uid,'cid':cid}) 

def add_employee(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)
        if request.POST:
            email=request.POST['email']
            password=request.POST['password']
            role=request.POST['role']
            uid=User.objects.create(email=email,role=role,password=password)  
            uid.save()  
            eid=Employee.objects.create(
                   user_id=uid,                
                firstname=request.POST['firstname'],               
                lastname=request.POST['lastname'],
                contact=request.POST['contact'],
                birthdate=request.POST['birthdate'],
                joiningdate=request.POST['joiningdate'],
                salary=request.POST['salary'],
                job_profile=request.POST['job_profile'],
                marital_status=request.POST['marital_status'],
                address=request.POST['address'],
                gender=request.POST['gender'],
                id_proof=request.FILES['id_proof'],
                profile_pic=request.FILES['profile_pic'],
                )
            

            if eid:            
                e_all= Employee.objects.all()
                print("+++++++++++++++++",e_all)
                return render(request,"CEO/all_employee.html",{"e_all":e_all,"uid":uid,'cid':cid})
        else:
            return render(request,"CEO/add_employee.html",{"uid":uid,'cid':cid})    
    else:
        return redirect('login')

def task(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)
        tid=Task.objects.all()
       
        in_progress_task=Task.objects.filter(status="in progress")
        return render(request,"CEO/task.html",{"uid":uid,'cid':cid,'tid':tid,'in_progress_task':in_progress_task})   

def mtask(request):
    if 'email' in request.session:
        uid=User.objects.get(email= request.session['email'])                   
        mid=Manager.objects.get(user_id=uid)          
        name=mid.firstname        
        tid=Task.objects.filter(firstname=name)        
        return render(request,"CEO/mtask.html",{"uid":uid,'mid':mid,'tid':tid})  
    else:
        return render(request,"CEO/mtask.html",{"uid":uid,'mid':mid}) 

def etask(request):
    if 'email' in request.session:
        uid=User.objects.get(email= request.session['email'])                   
        eid=Employee.objects.get(user_id=uid)          
        name=eid.firstname        
        tid=Task.objects.filter(firstname=name)        
        return render(request,"CEO/etask.html",{"uid":uid,'eid':eid,'tid':tid})  
    else:
        return render(request,"CEO/etask.html",{"uid":uid,'eid':eid}) 
    
def add_task(request): 
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid) 
        lid=Log.objects.all()
       
        if request.POST:
            all_user=User.objects.all()

                
            firstname=request.POST['firstname'] 
            title=request.POST['title']
            priority=request.POST['priority']
            description=request.POST['description']
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            tid=Task.objects.create(title=title,priority=priority,firstname=firstname,description=description,start_date=start_date,end_date=end_date)
            lid=Log.objects.create(user=uid, action_taken= uid.role+ ": has added a Task for " +tid.firstname)
            tid.save()

            return render (request, "CEO/add_task.html",{'cid':cid,'uid':uid,'tid':tid,'all_user':all_user,'lid':lid})
        else:
            return render (request, "CEO/add_task.html",{'cid':cid})
   
def c_edittask(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid) 
        tid=Task.objects.all() 
        lid=Log.objects.all()  
        print(":::::::::::",cid) 
       
        tid=Task.objects.get(title=id)
        print("=============",tid,id)

        if request.POST:
            # tid.firstname=request.POST['firstname']
            tid.title=request.POST['title']
            tid.description=request.POST['description']
            tid.created_at=request.POST['created_at']
            tid.end_date=request.POST['end_date']
            tid.priority=request.POST['priority']
            lid=Log.objects.create(user=uid, action_taken= uid.role+ ": has edited a Task for " +tid.firstname)
            tid.save()
            print("=============",tid)
            u_msg="Task updated Successfully"

            return render(request, 'CEO/c_edittask.html',{"uid":uid,'cid':cid,'tid':tid,'u_msg':u_msg,'lid':lid})
        else:
            return render(request, 'CEO/c_edittask.html',{"uid":uid,'cid':cid,'tid':tid})

def m_edittask(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])      
        mid=Manager.objects.get(user_id=uid)
        tid=Task.objects.all()       
        # tid=Task.objects.filter(title=id).values()
        tid=Task.objects.get(title=id)
        print("====================================",tid)
        if request.POST:
            tid.status=request.POST['status']
            tid.title=request.POST['title']
            tid.save()
    
       

        return render(request, 'CEO/m_edittask.html',{"uid":uid,'mid':mid,'tid':tid})

def e_edittask(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email'])      
        eid=Employee.objects.get(user_id=uid)
        tid=Task.objects.all()       
        # tid=Task.objects.filter(title=id).values()
        tid=Task.objects.get(title=id)
        print("====================================",tid)
        if request.POST:
            tid.status=request.POST['status']
            tid.title=request.POST['title']
            tid.save()
    
       

        return render(request, 'CEO/e_edittask.html',{"uid":uid,'eid':eid,'tid':tid})
       
def del_task(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email']) 
        cid=CEO.objects.get(user_id=uid)     
        tid=Task.objects.get(title=id) 
        lid=Log.objects.all()    
        lid=Log.objects.create(user=uid, action_taken= uid.role+ ": has deleted a Task for " +tid.firstname)
        tid.delete()  
      
        return render(request, 'CEO/task.html',{"uid":uid,'cid':cid,'lid':lid})

def m_del_task(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email']) 
        mid=Manager.objects.get(user_id=uid)     
        tid=Task.objects.get(title=id)   
        tid.delete()  
        u_msg="Task Deleted Successfully"  
        return redirect('mtask',{'u_msg':u_msg,'mid':mid})

def e_del_task(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email']) 
        eid=Employee.objects.get(user_id=uid)     
        tid=Task.objects.get(title=id)   
        tid.delete()  
        u_msg="Task Deleted Successfully"  
        return redirect('etask',{'u_msg':u_msg,'eid':eid})

def add_message(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid) 
        lid=Log.objects.all()    
        if request.POST:
            all_user=User.objects.all()

                
            firstname=request.POST['firstname'] 
            email=request.POST['email']
            message=request.POST['message']
          
          
            msg_id=Message.objects.create(firstname=firstname,email=email,message=message)
            lid=Log.objects.create(user=uid, action_taken= uid.role+ ": has sent message to " +msg_id.firstname)
            msg_id.save()
            return render (request, "CEO/add_message.html",{'cid':cid,'uid':uid,'msg_id':msg_id,'all_user':all_user,'lid':lid})
        else:
            return render (request, "CEO/add_message.html",{'cid':cid})

def m_add_message(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        mid=Manager.objects.get(user_id=uid) 
        if request.POST:
            all_user=User.objects.all()

                
            firstname=request.POST['firstname'] 
            email=request.POST['email']
            message=request.POST['message']
          
          
            msg_id=Message.objects.create(firstname=firstname,email=email,message=message)
            msg_id.save()
            return render (request, "CEO/m_add_message.html",{'mid':mid,'uid':uid,'msg_id':msg_id,'all_user':all_user})
        else:
            return render (request, "CEO/m_add_message.html",{'mid':mid})

def e_add_message(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        eid=Employee.objects.get(user_id=uid) 
        if request.POST:
            all_user=User.objects.all()

                
            firstname=request.POST['firstname'] 
            email=request.POST['email']
            message=request.POST['message']
          
          
            msg_id=Message.objects.create(firstname=firstname,email=email,message=message)
            msg_id.save()
            return render (request, "CEO/e_add_message.html",{'eid':eid,'uid':uid,'msg_id':msg_id,'all_user':all_user})
        else:
            return render (request, "CEO/e_add_message.html",{'eid':eid})

def all_message(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)
        allmsg_id=Message.objects.all()
         
        
       
        return render(request,"CEO/all_message.html",{"uid":uid,'cid':cid,'allmsg_id':allmsg_id,})  

def m_all_message(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        mid=Manager.objects.get(user_id=uid) 
        msg_id=Message.objects.all()
        name=mid.firstname        
        msg_id=Message.objects.filter(firstname=name) 
       
        return render(request,"CEO/m_all_message.html",{"uid":uid,'mid':mid,'msg_id':msg_id,}) 

def e_all_message(request):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        eid=Employee.objects.get(user_id=uid) 
        msg_id=Message.objects.all()
        name=eid.firstname        
        msg_id=Message.objects.filter(firstname=name) 
       
        return render(request,"CEO/e_all_message.html",{"uid":uid,'eid':eid,'msg_id':msg_id,}) 

def edit_message(request,id):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        cid=CEO.objects.get(user_id=uid)
        lid=Log.objects.all() 
       
        msg_id=Message.objects.get(email=id)
       
        if request.POST:         
            msg_id.message=request.POST['message']
            msg_id.email=request.POST['email']
            lid=Log.objects.create(user=uid, action_taken= uid.role+ ": has edited message for " +msg_id.firstname)
            msg_id.save()
            print("++++++++",msg_id)

            u_msg="Message updated Successfully"
            allmsg_id=Message.objects.all()
            return render(request, 'CEO/all_message.html',{"uid":uid,'allmsg_id':allmsg_id,'cid':cid,'msg_id':msg_id,'u_msg':u_msg,'lid':lid})
        else:
            return render(request, 'CEO/edit_message.html',{"uid":uid,'cid':cid,'msg_id':msg_id})

def m_edit_message(request,id):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        mid=Manager.objects.get(user_id=uid) 
       
        emsg_id=Message.objects.get(email=id)
       
        if request.POST:         
            emsg_id.message=request.POST['message']
            emsg_id.status=request.POST['status']
            emsg_id.save()
            print("++++++++",emsg_id)

            u_msg="Message updated Successfully"
            return render(request, 'CEO/m_edit_message.html',{"uid":uid,'mid':mid,'emsg_id':emsg_id,'u_msg':u_msg})
        else:
            return render(request, 'CEO/m_edit_message.html',{"uid":uid,'mid':mid,'emsg_id':emsg_id})

def e_edit_message(request,id):
    if 'email' in request.session:
        uid = User.objects.get(email= request.session['email'])      
        eid=Employee.objects.get(user_id=uid) 
       
        emsg_id=Message.objects.get(email=id)
       
        if request.POST:         
            emsg_id.message=request.POST['message']
            emsg_id.status=request.POST['status']
            emsg_id.save()
            print("++++++++",emsg_id)

            u_msg="Message updated Successfully"
            return render(request, 'CEO/e_edit_message.html',{"uid":uid,'eid':eid,'emsg_id':emsg_id,'u_msg':u_msg})
        else:
            return render(request, 'CEO/e_edit_message.html',{"uid":uid,'eid':eid,'emsg_id':emsg_id})


def delete_message(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email']) 
        cid=CEO.objects.get(user_id=uid)     
        msg_id=Message.objects.get(email=id)
        msg_id.delete()
        lid=Log.objects.create(user=uid, action_taken= ": has deleted message ") 
        u_msg="Message updated Successfully"
         
             
        return render(request, 'CEO/all_message.html',{"uid":uid,'cid':cid,'msg_id':msg_id,'lid':lid,'u_msg':u_msg})

def m_delete_message(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email']) 
        mid=Manager.objects.get(user_id=uid)  
        msg_id=Message.objects.get(email=id)  
        msg_id.delete()  
        u_msg="Message deleted Successfully"  
        return redirect('m_all_message',{'u_msg':u_msg,'mid':mid})

def e_delete_message(request,id):
    if "email" in request.session:
        uid = User.objects.get(email= request.session['email']) 
        eid=Employee.objects.get(user_id=uid) 
        msg_id=Message.objects.get(email=id)  
        msg_id.delete()  
        u_msg="Message deleted Successfully"  
        return redirect('e_all_message',{'u_msg':u_msg,'eid':eid})

class CalendarView(generic.ListView):
    model = Event
    template_name = 'CEO/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        all_events=Event.objects.all()
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['all_events'] = all_events
        
        return context

    

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

# def event(request, event_id=None):
#     instance = Event()
#     if event_id:
#         instance = get_object_or_404(Event, pk=event_id)
#     else:
#         instance = Event()

#     form =EventForm(request.POST or None, instance=instance)
#     if request.POST and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('calendar'),{'form': form})
#     return render(request, 'CEO/event.html', {'form': form})

def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
           
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'CEO/event.html', {'form': form})



def event_details(request):
    event = Event.objects.all()    
    context = {"event": event}
    return render(request, "CEO/event_details.html", context)


def new_calendar(request):
    return render(request, "CEO/new_calendar.html")