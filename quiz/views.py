import random
import csv, io
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView
from .forms import QuestionForm
from .models import Quiz, Category, Progress, Sitting, Question, Subscription, Paper
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from .models import Student, Contact, Coordinator, School_register, Invoice,Syllabus,Standard
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from quiz.tokens import account_activation_token
from django.contrib.auth.models import User
from mcq.models import MCQQuestion,Answer

my_list =[]
my_answers= []
my_ques= []
dict_pdf={}
lst=[]
#and user.email_confirmed
# def loginhandle(request):
#     if(request.method=='POST'):
#         username=request.POST['email']
#         password=request.POST['pass']
#         user=authenticate(username=username, password=password)
#         print(user)
#         if(user):
#             if(user.is_active ):
#                 login(request,user)
#                 messages.success(request,"Successfully logged in")
#                 return render(request,"loginhandle.html")

#         else:
#             messages.error(request,"User is not registered")

#     return render(request,"loginhandle.html")


# def logouthandle(request):
# 	logout(request)
# 	messages.success(request,"Successfully logged out")
# 	return redirect('/')

#def home(request):
#    return render(request,"home.html")


import hashlib
import hmac
import base64



def invoice_view(request):
    p=request.user
    print(p)
    print(request.user.username)
    stud=request.user.username
    val=Invoice.objects.filter(student=stud)
    print(val)

    return render(request,"invoice.html",{'val':val})
    # q=Invoice.objects.get(student=request.user)

def invoice_ind(request,sub_order_id):
    l=Invoice.objects.get(order_id=sub_order_id)
    return render(request,"invoice_ind.html",{'l':l})

def home(request):
    return render(request,'start.html')

def changeslot(request):


    if request.method=='POST':
        student = request.user
        sub=Student.objects.get(pk=student.id)

        change = request.POST['change']


        if change=='gk':

            return render(request,'gk.html')
        if change=='math':

            return render(request,'math.html')
        if change=='english':

            return render(request,'english.html')
        if change=='reasoning':

            return render(request,'reasoning.html')
        if change=='science':

            return render(request,'science.html')
        if change=='cyber':

            return render(request,'cyber.html')

        #return render(request,'bookafterchange.html',context)

    return render(request,'changeslot.html')

@csrf_exempt
def response_changeslot(request):


        postData = {
        "orderId" : request.POST['orderId'],
        "orderAmount" : request.POST['orderAmount'],
        "referenceId" : request.POST['referenceId'],
        "txStatus" : request.POST['txStatus'],
        "paymentMode" : request.POST['paymentMode'],
        "txMsg" : request.POST['txMsg'],
        "signature" : request.POST['signature'],
        "txTime" : request.POST['txTime']
        }

        print(postData)
        signatureData = ""
        signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + postData['txStatus'] + postData['paymentMode'] + postData['txMsg'] + postData['txTime']

        message = signatureData.encode('utf-8')
      # get secret key from your config
        secret = secretKey.encode('utf-8')
        computedsignature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode('utf-8')

        context = {
        'postData':postData,
        'computedsignature':computedsignature,
        'is_paid':False,
        }


        print(request)
        if computedsignature==postData['signature']:

            context['is_paid']= True


        return render(request,'response2.html', context)




def changeafterbook(request):

    if request.method=='POST':
        mode = "PROD"

        quiz = request.POST['slot']

        student = request.user
        sub=Student.objects.get(pk=student.id)

        sub.quiz_to_change = quiz
        sub.save(update_fields=['quiz_to_change'])

        student = request.user
        sub=Student.objects.get(pk=student.id)

        sub.order_number = sub.order_number+1
        sub.save(update_fields=['order_number'])

        temp = str(request.user.username)+str('_')+str(request.user.order_number)

        postData = {
                  "appId" : '58782c06ab69a52be2f34bd7b28785',
                  "orderId" : temp,
                  "orderAmount" : '30',
                  "orderCurrency" : 'INR',
                  "orderNote" : "payment",
                  "customerName" : str(request.user.first_name),
                  "customerPhone" : str(request.user.number),
                  "customerEmail" : str(request.user.email),
                  "returnUrl" : 'http://127.0.0.1:8000/response_changeslot/',
                  "notifyUrl" : 'https://github.com/'
        }


        # dict_pdf={"appId" : '21845d9c06b478a19ac3040ce54812',
        #           "orderId" : temp,
        #           "orderAmount" : '30',
        #           "orderCurrency" : 'INR',
        #           "orderNote" : "payment",
        #           "customerName" : str(request.user.first_name),
        #           "customerPhone" : str(request.user.number),
        #           "customerEmail" : str(request.user.email),
        #           "returnUrl" : 'http://127.0.0.1:8000/response_changeslot/',
        #           "notifyUrl" : 'https://github.com/'
        #           }
        print(postData)
        # print(dict_pdf)
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:

            signatureData += key+postData[key]
        message = signatureData.encode('utf-8')
          #get secret key from your config
        secret = secretKey.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode("utf-8")
        if mode == 'PROD':

            url = "https://www.cashfree.com/checkout/post/submit"
        else:
            url = "https://prod.cashfree.com/billpay/checkout/post/submit"

        context = {
            'postData' : postData,
            'url' : url,
            'signature' :signature,

        }

        return render(request,'request.html', context)
        print(quiz)

    return render(request,'changeslot.html')

def invoice(request,dict_pdf):
    # sub=Student.objects.get(pk=student.id)
    order_id=dict_pdf['orderId']
    order_amount=dict_pdf['orderAmount']
    reference_id=dict_pdf['referenceId']
    payment_mode=dict_pdf['paymentMode']
    pay_time=dict_pdf['txTime']
    k=order_id.split("_")
    student=k[0]
    inv=Invoice(student=student,order_id=order_id,order_amount=order_amount,reference_id=reference_id,payment_mode=payment_mode,pay_time=pay_time)
    # sub.email=request.user.email
    inv.save()

def bookslot(request):


    student = request.user
    print(student)
    sub=Student.objects.get(pk=student.id)
    if(sub.mathsolym==True):
        sub.final_mathsolym=sub.mathsolym
    if(sub.scienceolym==True):
        sub.final_scienceolym=sub.scienceolym
    if(sub.englisholym==True):
        sub.final_englisholym=sub.englisholym
    if(sub.reasoningolym==True):
        sub.final_reasoningolym=sub.reasoningolym
    if(sub.cyberolym==True):
        sub.final_cyberolym= sub.cyberolym
    if(sub.generalolym==True):
        sub.final_generalolym=sub.generalolym
    print ("hi")
    print(request.user.first_name)
    # if(mathsolym==True):
    #     lst.append("ISMO")
    # if(scienceolym==True):
    #     lst.append("ISSO")
    # if(englisholym==True):
    #     lst.aapend("ISEO")
    # if(reasoningolym==True):
    #     lst.append("ISCTO")
    # if(cyberolym==True):
    #     lst.append("ISCO")
    # if(generalolym==True):
    #     lst.append("ISGKO")
    # invoice(request,student,lst)
    sub.save(update_fields=['final_mathsolym','final_scienceolym','final_englisholym','final_reasoningolym','final_cyberolym','final_generalolym'])





    if request.method=='POST':
        student = request.user
        sub=Student.objects.get(pk=student.id)
        if   'scienceslot' in request.POST:


            scienceslot = request.POST['scienceslot']
        else:
            scienceslot='nil'


        if  'englishslot'  in request.POST:

            englishslot = request.POST['englishslot']
        else:
            englishslot='nil'

        if  'cyberslot' in  request.POST:

            cyberslot = request.POST['cyberslot']
        else:
            cyberslot='nil'

        if  'mathslot' in request.POST:

            mathslot = request.POST['mathslot']
        else:
            mathslot='nil'

        if 'reasoningslot' in  request.POST:

            reasoningslot = request.POST['reasoningslot']
        else:
            reasoningslot='nil'

        if  'gkslot' in  request.POST:

            gkslot = request.POST['gkslot']
        else:
            gkslot='nil'

        print(scienceslot,mathslot,reasoningslot,gkslot,englishslot,cyberslot)

        if scienceslot !='nil':
            sq,st =scienceslot.split('@', 1)

            sub.sciencequiz = sq
            sub.sciencetime= st
            sub.save(update_fields=['sciencequiz','sciencetime'])

        print(englishslot)
        if str(englishslot) != str("nil"):

            sq,st = englishslot.split('@', 1)
            sub.englishquiz = sq
            sub.englishtime= st
            sub.save(update_fields=['englishquiz','englishtime'])

        if cyberslot !='nil':
            sq,st = cyberslot.split('@', 1)
            sub.cyberquiz = sq
            sub.cybertime= st
            sub.save(update_fields=['cyberquiz','cybertime'])

        if mathslot !='nil':
            sq,st = mathslot.split('@', 1)
            sub.mathquiz = sq
            sub.mathtime= st
            sub.save(update_fields=['mathquiz','mathtime'])

        if gkslot !='nil':
            sq,st = gkslot.split('@', 1)
            sub.gkquiz = sq
            sub.gktime= st
            sub.save(update_fields=['gkquiz','gktime'])

        if reasoningslot !='nil':
            sq,st = reasoningslot.split('@', 1)
            sub.reasoningquiz = sq
            sub.reasoningtime= st
            sub.save(update_fields=['reasoningquiz','reasoningtime'])


        sub.mathsolym = False;
        sub.scienceolym = False;
        sub.englisholym = False;
        sub.reasoningolym = False;
        sub.cyberolym = False;
        sub.generalolym = False;
        sub.save(update_fields=['mathsolym','scienceolym','englisholym','reasoningolym','cyberolym','generalolym'])



        messages.success(request, 'Slot booked successfully')
        return render(request,'index.html')



    return render(request,'book.html')

def profile(request):
    return render(request,'dashboard.html')

secretKey = "bb221fbe28841cb1a7eb30599b5dcad2a3e8dae2"
#@app.route('/request', methods=["POST"])
def handlerequest(request):

    mode = "PROD" # <-------Change to TEST for test server, PROD for production
    print('win')

    if request.method =='POST':
        print('lost')

        postData = {
                  "appId" : '58782c06ab69a52be2f34bd7b28785',
                  "orderId" : request.POST['orderId'],
                  "orderAmount" : request.POST['orderAmount'],
                  "orderCurrency" : 'INR',
                  "orderNote" : "payment",
                  "customerName" : request.user.first_name,
                  "customerPhone" : request.user.number,
                  "customerEmail" : request.user.email,
                  "returnUrl" : 'http://127.0.0.1:8000/response/',
                  "notifyUrl" : 'https://github.com/'
        }
        print(postData)
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:

            signatureData += key+postData[key]
        message = signatureData.encode('utf-8')
          #get secret key from your config
        secret = secretKey.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode("utf-8")
        if mode == 'PROD':

            url = "https://www.cashfree.com/checkout/post/submit"
        else:
            url = "https://prod.cashfree.com/billpay/checkout/post/submit"

        context = {
            'postData' : postData,
            'url' : url,
            'signature' :signature
        }
    #    context
    #    context['url']= url
    #    context['signature']= signature
        return render(request,'request.html', context)


    return render(request,"sub.html")


#@app.route('/response', methods=["GET","POST"])
@csrf_exempt
def handleresponse(request):

    postData = {
    "orderId" : request.POST['orderId'],
    "orderAmount" : request.POST['orderAmount'],
    "referenceId" : request.POST['referenceId'],
    "txStatus" : request.POST['txStatus'],
    "paymentMode" : request.POST['paymentMode'],
    "txMsg" : request.POST['txMsg'],
    "signature" : request.POST['signature'],
    "txTime" : request.POST['txTime']
    }

    dict_pdf = {
    "orderId" : postData['orderId'],
    "orderAmount" : postData['orderAmount'],
    "referenceId" : postData['referenceId'],
    "txStatus" : postData['txStatus'],
    "paymentMode" : postData['paymentMode'],
    "txMsg" : postData['txMsg'],
    "signature" : postData['signature'],
    "txTime" : postData['txTime']
    }

    invoice(request,dict_pdf)




    # dict_pdf = {
    # "orderId" : request.POST['orderId'],
    # "orderAmount" : request.POST['orderAmount'],
    # "referenceId" : request.POST['referenceId'],
    # "txStatus" : request.POST['txStatus'],
    # "paymentMode" : request.POST['paymentMode'],
    # "txMsg" : request.POST['txMsg'],
    # "signature" : request.POST['signature'],
    # "txTime" : request.POST['txTime']
    # }

    print(postData)

    print("------------------")
    print(dict_pdf)
    signatureData = ""
    signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + postData['txStatus'] + postData['paymentMode'] + postData['txMsg'] + postData['txTime']

    message = signatureData.encode('utf-8')
  # get secret key from your config
    secret = secretKey.encode('utf-8')
    computedsignature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode('utf-8')

    context = {
    'postData':postData,
    'computedsignature':computedsignature,
    'is_paid':False,
    }


    print(request)
    if computedsignature==postData['signature']:

        context['is_paid']= True

        """
        student = request.user
        sub=Student.objects.get(pk=student.id)
        if(sub.mathsolym==True):
            sub.final_mathsolym=mathsolym
        if(sub.scienceolym==True):
            sub.final_scienceolym=scienceolym
        if(sub.englisholym==True):
            sub.final_englisholym=englisholym
        if(sub.reasoningolym==True):
            sub.final_reasoningolym=reasoningolym
        if(sub.cyberolym==True):
            sub.final_cyberolym= cyberolym
        if(sub.generalolym==True):
            sub.final_generalolym=generalolym
        print ("hi")
        print(request.user.first_name)
        sub.save(update_fields=['final_mathsolym','final_scienceolym','final_englisholym','final_reasoningolym','final_cyberolym','final_generalolym'])


        sub.mathsolym = False;
        sub.scienceolym = False;
        sub.englisholym = False;
        sub.reasoningolym = False;
        sub.cyberolym = False;
        sub.generalolym = False;
        sub.save(update_fields=['mathsolym','scienceolym','englisholym','reasoningolym','cyberolym','generalolym'])
        """






    return render(request,'response.html', context)

from django.http import HttpResponse


def subscribe(request):
    print ("hibhai")
    mode = "PROD"
    student = request.user
    stud=Student.objects.get(pk=student.id)
    if request.method=='POST':
        print ("hibhaiji")
        student = request.user
        sub=Student.objects.get(pk=student.id)
        mathsolym=request.POST.get('mathsolym', False)
        scienceolym=request.POST.get('scienceolym',False)
        englisholym=request.POST.get('englisholym', False)
        reasoningolym=request.POST.get('reasoningolym', False)
        cyberolym=request.POST.get('cyberolym', False)
        generalolym=request.POST.get('generalolym', False)

        if(sub.mathsolym==False):
            sub.mathsolym=mathsolym
        if(sub.scienceolym==False):
            sub.scienceolym=scienceolym
        if(sub.englisholym==False):
            sub.englisholym=englisholym
        if(sub.reasoningolym==False):
            sub.reasoningolym=reasoningolym
        if(sub.cyberolym==False):
            sub.cyberolym= cyberolym
        if(sub.generalolym==False):
            sub.generalolym= generalolym

        print ("hi")
        print(request.user.first_name)
        sub.save(update_fields=['mathsolym','scienceolym','englisholym','reasoningolym','cyberolym','generalolym'])

        print('lost')


        student = request.user
        sub=Student.objects.get(pk=student.id)

        sub.order_number = sub.order_number+1
        sub.save(update_fields=['order_number'])

        temp = str(request.user.username)+str('_')+str(request.user.order_number)

        print(temp)

        postData = {
                  "appId" : '58782c06ab69a52be2f34bd7b28785',
                  "orderId" : temp,
                  "orderAmount" : request.POST['orderAmount'],
                  "orderCurrency" : 'INR',
                  "orderNote" : "payment",
                  "customerName" : str(request.user.first_name),
                  "customerPhone" : str(request.user.number),
                  "customerEmail" : str(request.user.email),
                  "returnUrl" : 'http://127.0.0.1:8000/response/',
                  "notifyUrl" : 'https://github.com/'
        }


        print(postData)

        # lst2=[]
        # lst.append(postData)
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:

            signatureData += key+postData[key]
        message = signatureData.encode('utf-8')
          #get secret key from your config
        secret = secretKey.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode("utf-8")
        if mode == 'PROD':

            url = "https://www.cashfree.com/checkout/post/submit"
        else:
            url = "https://prod.cashfree.com/billpay/checkout/post/submit"

        context = {
            'postData' : postData,
            'url' : url,
            'signature' :signature,
            'mathsolym':mathsolym,
            'scienceolym':scienceolym,
            'englisholym':englisholym,
            'reasoningolym':reasoningolym,
            'cyberolym':cyberolym,
            'generalolym': generalolym

        }

        return render(request,'request.html', context)


    return render(request,"subscriptions2.html",{'stud':stud})


def examdates(request):
    return render(request,"examdates.html")

def faqs(request):
    return render(request,"faqs.html")


# print(dict_pdf['orderId'])


def render_to_pdf(template_src,content_type={}):
    template=get_template(template_src)
    html=template.render(content_type)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")
    return None


# class ViewPDF(View):
#     def get(self, request , *args, **kwargs):
#         pdf=render_to_pdf('response.html',data)
#         return HttpResponse(pdf, content_type='application/pdf')


class DownloadPDF(View):
    def get(Self, request, *args, **kwargs):
        order_id = kwargs.get('sub_order_id')
        order_data = Invoice.objects.get(order_id=order_id)

        data = {
            'postData': {
                'orderId': order_data.order_id,
                'orderAmount':order_data.order_amount,
                'referenceId':order_data.reference_id,
                'paymentMode':order_data.payment_mode,
                'txTime': order_data.pay_time

            }
        }
        pdf=render_to_pdf('response.html', data)
        response= HttpResponse(pdf, content_type='application/pdf')
        filename= "Invoice_%s.pdf" %("12341231")
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response


# def doc_upload(request):
#     print(')))))))))))))))))))))))')
#     if(request.method=='POST'):
#         stud=request.user
#         school_id=request.POST.get('school_id'," ")
#         print("*******************")
#         print(request.POST)
#         prev_marksheet=request.POST.get('prev_marksheet'," ")
#         photo=request.POST.get('photo'," ")
#         if(school_id!=" "):
#             stud.idproof=school_id
#             stud.save(update_fields=['idproof'])
#         if(prev_marksheet!=" "):
#             stud.marksheet=prev_marksheet
#             stud.save(update_fields=['marksheet'])
#         if(photo!=" "):
#             stud.photograph=photo
#             stud.save(update_fields=['photograph'])
#         # stud.save(update_fields=['school_id','prev_marksheet','photo'])
#         messages.success(request, 'Documents successfully uploaded')
#     return render(request,"dashboard.html")



from django.contrib.auth.hashers import check_password

def change_password(request):
    if(request.method=="POST"):
        student=request.user
        oldpass=request.POST['oldpass']
        newpass=request.POST['newpass']
        newpass2=request.POST['newpass2']

        print( request.user.password)
        matchcheck= check_password(oldpass, request.user.password)
        print(matchcheck)
        print(oldpass)

        if(newpass==newpass2):

            if matchcheck:

                student.set_password(newpass)
                student.save(update_fields=['password'])
                messages.success(request, 'Password changed successful')
            else:
                messages.error(request, 'Wrong user password ')

        else:
            messages.error(request, 'Password entered do not match')

    return render(request,'changepassword.html')


def update_student(request):
    sub = request.user
    # print(student)
    # sub=Student.objects.get(pk=student.id)
    if(request.method=="POST"):

        print(request.POST)

        sub.country =request.POST['country']
        sub.address = request.POST['address']
        sub.street= request.POST['street']
        sub.country= request.POST['country']
        sub.state=request.POST['state']
        sub.school=request.POST['school']
        sub.school_state = request.POST['school_state']
        sub.school_address=request.POST['school_address']
        sub.school_city=request.POST['school_city']
        sub.pincode = request.POST['pincode']
        sub.number=request.POST['number']

        sub.save(update_fields=['country','address',"street",'state','school','school_state',"school_address",'school_city','pincode','number'])
        return render(request,"dashboard.html")

    return render(request,"subscriptions2.html")

@csrf_exempt
def uploadfiles(request):

    stud=request.user
    if(request.method=='POST'):

        idproof=request.FILES.get('idproof'," ")
        print("*******************")
        # print(request.POST)
        marksheet=request.FILES.get('marksheet'," ")
        photograph=request.FILES.get('photograph'," ")
        print(marksheet)
        print(idproof)
        print(photograph)
        print("4444444444444444444444444444")
        if(idproof!=" "):
            stud.idproof=idproof
            stud.idproof_date="idproof"
            stud.save(update_fields=['idproof','idproof_date'])
        if(marksheet!=" "):
            stud.marksheet=marksheet
            stud.marksheet_date="marksheet"
            stud.save(update_fields=['marksheet','marksheet_date'])
        if(photograph!=" "):
            stud.photograph=photograph
            stud.photograph_date="photograph"
            stud.save(update_fields=['photograph','photograph_date'])
        # stud.save(update_fields=['school_id','prev_marksheet','photo'])
        messages.success(request, 'Documents successfully uploaded')
    return render(request,"dashboard.html",{'stud':stud})




def contact(request):
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        phonenum=request.POST['phonenum']
        message=request.POST['message']
        coordinate=Contact(name=name,email=email,phonenum=phonenum,message=message)
        messages.success(request, ('You will be contacted soon by our team'))
        coordinate.save()

    return render(request,"contact.html")


def coordinator(request):
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        phonenum=request.POST['phonenum']
        message=request.POST['message']
        coordinate=Coordinator(name=name,email=email,phonenum=phonenum,message=message)
        coordinate.save()
        messages.success(request, ('Request for Coordinator received successfully'))
        return render(request,"coordinator.html")

    return render(request,"coordinator.html")


def register_school(request):
    if(request.method=='POST'):
        button=request.POST['button']
        name=request.POST['name']
        email=request.POST['email']
        country=request.POST['country']
        contact=request.POST['contact']
        school_name=request.POST['school_name']
        school_address=request.POST['school_address']
        school_city=request.POST['school_city']
        school_pincode=request.POST['school_pincode']
        school_website=request.POST['school_website']
        school_email=request.POST['school_email']
        pname=request.POST['pname']
        pmobile=request.POST['pmobile']
        exammode=request.POST['exammode']
        if(School_register.objects.filter(school_email=school_email).exists()):
            messages.warning(request,"Email already exists")
        else:
            school_r=School_register(type=button, name=name, email=email,country=country,contact=contact, school_name=school_name,school_address=school_address, school_city=school_city, school_pincode=school_pincode,school_website=school_website,school_email=school_email, pname=pname, pmobile=pmobile, exammode=exammode)
            school_r.save()
            messages.success(request, 'School Registered successfully')


    return render(request,"applyschool.html")



def register(request):
    if(request.method=='POST'):

        ref_code = request.POST.get('ref_code', '000')
        # print(ref_code, "ref_Code")
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username= request.POST['username']
        parent_name = request.POST['parent_name']
        dob = request.POST['dob']
        country =request.POST['country']
        address = request.POST['address']
        street= request.POST['street']
        state=request.POST['state']
        school=request.POST['school']
        school_state = request.POST['school_state']
        school_address=request.POST['school_address']
        school_city=request.POST['school_city']
        pincode = request.POST['pincode']
        number=request.POST['number']
        email = request.POST['email']
        password =request.POST['password']
        standard = request.POST['standard']

        if(Student.objects.filter(email=email).exists()):
            messages.warning(request,"Email already exists")
        else:
            if(Student.objects.filter(username=username).exists()):
                messages.warning(request,"Username already exists")
            else:
                student_context=Student(ref_code = ref_code ,first_name=first_name,username=username, last_name=last_name,parent_name = parent_name,dob = dob,country= country,address= address,street=street,state=state,school=school,school_state= school_state,school_address= school_address,school_city= school_city,pincode=pincode,number=number,email=email,standard= standard)
                student_context.set_password(password)
                student_context.save()
                # messages.success(request, 'Registration successful')
                print("okkkkkkk")


                current_site = get_current_site(request)
                subject = 'Activate Your Crest Olympiad Account'
                message = render_to_string('account_activation_email.html', {
                'user': student_context,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(student_context.pk)),
                'token': account_activation_token.make_token(student_context),
                 })
                send_mail(subject, message,settings.EMAIL_HOST_USER,[student_context.email,],fail_silently=False,)


                messages.success(request, ('Please Confirm your email to complete registration.'))
                return render(request,"login.html")


    return render(request,'applyindividual.html')



class ActivateAccount(View):


    def get(self, request, uidb64, token, *args, **kwargs):
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = Student.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, Student.DoesNotExist):
                user = None

            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.email_confirmed = True
                user.save()
                login(request, user)
                messages.success(request, ('Your account has been confirmed.'))
                return redirect('/')
            else:
                messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
                return redirect('/')



class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


class QuizListView(ListView):
    model = Quiz
    # @login_required
    def get_queryset(self):

        bro = Quiz.objects.all()
        print(bro)
        print("wd2d")
        print(self)
        queryset = super(QuizListView, self).get_queryset()
def mock(request):
    if request.user.is_authenticated:
        all_quizzes = Quiz.objects.all()
        print(all_quizzes)

        quizlist=[]
        for quiz in all_quizzes:

            if quiz.title.find('_')!=-1:
                _,quiz_title = quiz.title.split('_', 1)
            else:
                quiz_title= quiz.title

            #print(quiz)
            #print(quiz.title[0:2])

            #print(quiz_title[0:2])
            b = quiz_title[2:]

            #print(request.user.b)
            print(quiz_title[2:])
            if str(request.user.standard)==str(quiz_title[0:2]):
                quizlist.append(quiz)


        return render(request, 'quiz_mock.html', {"quiz_list": quizlist})
    else:
        return redirect('loginhandle')



def myquiz(request):

    all_quizzes = Quiz.objects.all()
    # print(all_quizzes)

    quizlist=[]
    for quiz in all_quizzes:

        if quiz.title.find('_')!=-1:
            _,quiz_title = quiz.title.split('_', 1)
        else:
            quiz_title= quiz.title

        #print(quiz)
        #print(quiz.title[0:2])

        #print(quiz_title[0:2])
        b = quiz_title[2:]

        # print(request.user.standard)
        # print(quiz_title[0:2])
        if str(request.user.standard if len(request.user.standard) > 1 else "0" + str(request.user.standard))==str(quiz_title[0:2]):
            if quiz_title[2:]=='mathsolym' and request.user.final_mathsolym==True:
                quizlist.append(quiz)
            if quiz_title[2:]=='scienceolym' and request.user.final_scienceolym==True:
                quizlist.append(quiz)
            if quiz_title[2:]=='englisholym' and request.user.final_englisholym==True:
                quizlist.append(quiz)
            if quiz_title[2:]=='generalolym' and request.user.final_generalolym==True:
                quizlist.append(quiz)
            if quiz_title[2:]=='cyberolym' and request.user.final_cyberolym==True:
                quizlist.append(quiz)
            if quiz_title[2:]=='reasoningolym' and request.user.final_reasoningolym==True:
                quizlist.append(quiz)
    print(quizlist)
    return render(request, 'quiz_list.html', {"quiz_list": quizlist})



class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CategoriesListView(ListView):
    model = Category


class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset()\
                                               .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset

    class Meta:
        pass


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] =\
            context['sitting'].get_questions(with_answers=True)
        return context


class QuizTake(TemplateView):
    template_name = 'question.html'


    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])


        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,self.quiz)

            allquestion = self.quiz.get_questions()

            self.progress = self.sitting.progress()
            print(allquestion)
            global bro
            progress, c = Progress.objects.get_or_create(user=self.request.user)
            if(request.method=='POST'):

                bro = 0
                for ques in allquestion:
                    # if(request.POST==None):
                    #     self.question = ques
                    #     answer = Answer.objects.get(id=guess)
                    #     self.sitting.add_incorrect_question(self.question)
                    #     progress.update_score(self.question, 0, 1)
                    # else:
                    guess =request.POST.get('%s'%ques.id,00)
                    print(guess)
                    
                    self.question = ques
                    if(guess==00):
                        print("*************************************")
                        # self.sitting.add_incorrect_question(self.question)
                        # progress.update_score(self.question, 0, 1)
                    else:
                        answer = Answer.objects.get(id=guess)
                        print(answer)
                        print("*************************************")

                        if answer.correct is True:
                            bro = bro+1
                            self.sitting.add_to_score(1)
                            progress.update_score(self.question, 1, 1)
                        else:
                            self.sitting.add_incorrect_question(self.question)
                            progress.update_score(self.question, 0, 1)

                    self.previous = {}

                    self.sitting.add_user_answer(self.question, guess)

                print(bro)
                return self.final_result_user()

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    # def get_form(self, form_class=QuestionForm):
    #     if self.logged_in_user:
    #         self.question = self.sitting.get_first_question()
    #         self.progress = self.sitting.progress()
    #     return form_class(**self.get_form_kwargs())

    # def get_form_kwargs(self):
    #     kwargs = super(QuizTake, self).get_form_kwargs()

    #     return dict(kwargs, question=self.question ,my_ques = my_ques)


    answers = []
    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        # print(self.quiz.get_questions())
        allquestion = self.quiz.get_questions()
        my_answers=[]
        d=[]
        q = {
                'question': '',
                'answers': []
            }
        for ques in allquestion:
            # q = {}
            my_answers=[]
            q = {
                'question': '',
                'answers': []
            }
            q['question'] = ques
            ques_c = MCQQuestion.objects.get(id = int(ques.id))
            ques_choices = [x for x in ques_c.get_answers_list()]
            # q[ques.content]=ques_choices
            # print(ques_choices)
            for choice in ques_choices:
                my_answers.append(choice)
            # print(q)
                # q[ques.content]=choice[1]
            q['answers']=my_answers
            # print(q)
                # q.answers.append(choice[1])
            d.append(q)

        context['my_ques'] = d
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        context['q_length'] = len(d)
        return context


    def final_result_user(self):
        per = (bro/self.sitting.get_max_score)*100
        results = {
            'quiz': self.quiz,
            'score': bro,
            'max_score': self.sitting.get_max_score,
            'percent': per,
            'sitting': self.sitting,

            #'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, 'result.html', results)




def index(request):


    if request.user.is_authenticated:

        student = request.user
        print(student)
        sub=Student.objects.get(pk=student.id)


        if sub.quiz_to_change != "nil":
            temp1 = sub.quiz_to_change
            sq,st = temp1.split('@', 1)

            print (sq)
            print(st)
            temp = sq
            _,quiz = temp.split('_', 1)
            print(quiz)

            if ( quiz[2:]=='mathsolym'):

                sub.mathquiz = sq
                sub.mathtime= st
                sub.save(update_fields=['mathquiz','mathtime'])


            elif (quiz[2:]=='englisholym'):

                sub.englishquiz = sq
                sub.englishtime= st
                sub.save(update_fields=['englishquiz','englishtime'])

            elif (quiz[2:]=='scienceolym'):
                sub.sciencequiz = sq
                sub.sciencetime= st
                sub.save(update_fields=['sciencequiz','sciencetime'])


            elif (quiz[2:]=='generalolym'):
                sub.gkquiz = sq
                sub.gktime= st
                sub.save(update_fields=['gkquiz','gktime'])

            elif (quiz[2:]=='reasoningolym'):
                sub.reasoningquiz = sq
                sub.reasoningtime= st
                sub.save(update_fields=['reasoningquiz','reasoningtime'])

            elif (quiz[2:]=='cyberolym'):
                sub.cyberquiz = sq
                sub.cybertime= st
                sub.save(update_fields=['cyberquiz','cybertime'])

            sub.quiz_to_change = 'nil'
            sub.save(update_fields=['quiz_to_change'])


    return render(request, 'index.html', {})


def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.email_confirmed:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return render(request, 'index.html')
            else:
                messages.error(request, 'Email not confirmed yet!')
        else:
            messages.error(request,"User is not registered")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    print('logout function working')
    return redirect('loginhandle')


from tablib import Dataset
@permission_required('admin.can_add_log_entry')
def paper(request):
    # template="paper.html"
    # prompt={
    #     'order':'Order of CSV should be quiz_name,questions,option_1,option_2,option_3,option_4,correct'
    # }

    # if(request.method=='POST'):
    #     return render(request,template,prompt)
    if(request.method=='POST'):
        print("==========================================")
        csv_file=request.FILES['file']
        dataset= Dataset()
        data_set=dataset.load(csv_file.read(),format= 'xlsx')
        #io_string=io.StringIO(data_set)
        # next(io_string)
        print(data_set)
        for column in dataset:


            print(column[2])
            my = Quiz.objects.filter(title=column[2])
            stan = Standard.objects.filter(standard=column[11])
            print(stan[0])
            print(my)
            # print(my[0].id)
            pap= MCQQuestion(
                # id=column[0],
                content=column[0],
                category=my[0].category,
                #quiz=my[0].title,
                #explanation=column[3],
                standard=stan[0],
                answer_order= "content"
            )


            #pap.quiz.set(my[0].id)
            print(column[4],'4',column[6],'6',column[8],'8',column[10])
            pap.save()
            pap.quiz.set(my)
            is_corr = False
            if column[4]:
                is_corr=True


            one = Answer(question =pap , content = column[3] ,correct= is_corr)
            one.save()

            is_corr = False
            if column[6]:
                is_corr=True


            two = Answer(question =pap , content = column[5] ,correct= is_corr)
            two.save()

            is_corr = False
            if column[8]:
                is_corr=True


            three = Answer(question =pap , content = column[7] ,correct= is_corr)
            three.save()

            is_corr = False
            if column[10]:
                is_corr=True


            four = Answer(question =pap , content = column[9] ,correct= is_corr)
            four.save()

            # context={}
    return render(request,"paper.html")










def samplepaper(request,sub,std):
    tem = 'sample'+sub+std+'.html'
    return render(request,tem)






# def loginhandle(request):
#     if(request.method=='POST'):
#         username=request.POST['email']
#         password=request.POST['pass']
#         user=authenticate(username=username, password=password)
#         print(user)
#         if(user):
#             if(user.is_active ):
#                 login(request,user)
#                 messages.success(request,"Successfully logged in")
#                 return render(request,"loginhandle.html")

#         else:
#             messages.error(request,"User is not registered")

#     return render(request,"loginhandle.html")


# def logouthandle(request):
# 	logout(request)
# 	messages.success(request,"Successfully logged out")
# 	return redirect('/')


def awards(request):
    return render(request,'awards.html')


def syllabus(request,olympiad,std):
    a = Syllabus.objects.filter(olympiad_name=olympiad).filter(std=std)
    b = {'syllabus':a}
    if(olympiad == 'maths'):
        name1 = 'Mathematics'
    if(olympiad == 'gk'):
        name1 = 'General Knowledge'
    if(olympiad == 'ct'):
        name1 = 'Critical Thinking'
    if(olympiad == 'science'):
        name1 = 'Science'
    if(olympiad == 'english'):
        name1 = 'English'
    if(olympiad == 'cyber'):
        name1 = 'Cyber'
    c = {'name':name1}
    d = {'class':std}
    e = {'name1':olympiad}
    response = {**b,**c,**d,**e}
    return render(request,'syllabus.html',response)

def rankingcriteria(request):
    return render(request,'rankingcriteria.html')

def markingscheme(request,sub):
    tem = 'ms'+sub+'.html'
    return render(request,tem)

def subjectpage(request,sub):
    return render(request,'sub'+sub+'.html')

def workshops(request):
    return render(request,'workshops.html')

def examprep(request):
    return render(request,'examprep.html')

def career(request):
    return render(request,'career.html')

def privacypol(request):
    return render(request,'privacypol.html')
