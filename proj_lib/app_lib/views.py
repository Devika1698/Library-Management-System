from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import date

def home(request):
    return render(request,'home_page.html')

def admin(request):
    return render(request,'admin_page.html')

def student(request):
    return render(request,'student_page.html')

def stusign(request):
    form=StudentForm
    if request.method == 'POST':
        a = StudentForm(request.POST)
        if a.is_valid():
            fname = a.cleaned_data['fname']
            lname = a.cleaned_data['lname']
            uname = a.cleaned_data['uname']
            password = a.cleaned_data['password']
            enroll = a.cleaned_data['enroll']
            branch = a.cleaned_data['branch']
            b = Student_signup(fname=fname, lname=lname, uname=uname, password=password, enroll=enroll, branch=branch)
            b.save()
            return redirect(stulog)
        else:
            return HttpResponse("Signup failed")
    return render(request,'student_signup.html',{'form':form})

def adsign(request):
    form=AdminForm
    if request.method == 'POST':
        a = AdminForm(request.POST)
        if a.is_valid():
            fname = a.cleaned_data['fname']
            lname = a.cleaned_data['lname']
            uname = a.cleaned_data['uname']
            password = a.cleaned_data['password']
            b = Admin_signup(fname=fname, lname=lname, uname=uname, password=password)
            b.save()
            return redirect(adlog)
        else:
            return HttpResponse("Signup failed")
    return render(request,'admin_signup.html',{'form':form})

def stulog(request):
    form=Student_login
    if request.method=='POST':
        a=Student_login(request.POST)
        if a.is_valid():
            uname=a.cleaned_data['uname']
            password=a.cleaned_data['password']
            b=Student_signup.objects.all()
            for i in b:
                d=i.fname
                if(uname==i.uname and password==i.password):
                    return render(request, 'student_log2.html',{'d':d})
                else:
                    return HttpResponse('Login failed')
    return render(request, 'student_login.html',{'form':form})


def adlog(request):
    form=Admin_login
    if request.method=='POST':
        a=Admin_login(request.POST)
        if a.is_valid():
            uname=a.cleaned_data['uname']
            password=a.cleaned_data['password']
            b=Admin_signup.objects.all()
            for i in b:
                c=i.fname
                if(uname==i.uname and password==i.password):
                    return render(request, 'admin_log2.html',{'c':c})
                else:
                    return HttpResponse('Login failed')
    return render(request, 'admin_login.html',{'form':form})


def addbook(request):
    form=BookForm
    if request.method=='POST':
        a=BookForm(request.POST)
        if a.is_valid():
            bookname=a.cleaned_data['bookname']
            isbn=a.cleaned_data['isbn']
            author=a.cleaned_data['author']
            category=a.cleaned_data['category']
            b=BookModel(bookname=bookname, isbn=isbn, author=author, category=category)
            b.save()
            return HttpResponse("Book added succesfully")
        else:
            return HttpResponse("Book adding failed")
    return render(request, 'add_book.html', {'form':form})


def view_book(request):
    viewbook=BookModel.objects.all()
    return render(request,'view_book.html',{'viewbook':viewbook})


def issue_book(request):
    form=IssuedBookForm()
    if request.method=='POST':
        form=IssuedBookForm(request.POST)
        if form.is_valid():
            obj=IssuedBook()
            obj.enroll=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return HttpResponse("Book issued successfully..")
    return render(request, 'issue_book.html', {'form':form})


def view_issuedbook(request):
    issuedbook=IssuedBook.objects.all()
    l=[]
    for i in issuedbook:
        issdate=str(i.issuedate.day)+'-'+str(i.issuedate.month)+'-'+str(i.issuedate.year)
        expdate=str(i.expirydate.day)+'-'+str(i.expirydate.month)+'-'+str(i.expirydate.year)
        #fine caluculation
        days=(date.today()-i.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        books=list(BookModel.objects.filter(isbn=i.isbn))
        students=list(Student_signup.objects.filter(enroll=i.enroll))
        j=0
        for k in books:
            t=(students[j].get_name,students[j].enroll,books[j].bookname,books[j].author,issdate,expdate,fine)
            j=j+1
            l.append(t)
    return render(request,'view_issuedbook.html', {'l':l})


def viewissuedbookstud(request):
    student=Student_signup.objects.filter(id=request.user.id)
    issuedbook=IssuedBook.objects.filter(enroll=student[0].enroll)
    l1=[]
    l2=[]
    for i in issuedbook:
        books=BookModel.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user,student[0].enroll,student[0].branch,book.name,book.author)
            l1.append(t)
        issdate=str(i.issuedate.day)+'-'+str(i.issuedate.month)+'-'+str(i.issuedate.year)
        expdate=str(i.expirydate.day)+'-'+str(i.expirydate.month)+'-'+str(i.expirydate.year)
        #fine calculation
        days = (date.today() - i.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 10
        t=(issdate,expdate,fine)
        l2.append(t)
    return render(request,'view_issuedbookstud.html',{'l1':l1,'l2':l2})


def view_student(request):
    viewstudent = Student_signup.objects.all()
    return render(request, 'view_student.html', {'viewstudent': viewstudent})
