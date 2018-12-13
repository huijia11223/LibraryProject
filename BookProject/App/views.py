from django.shortcuts import render,redirect
from .forms.login import LoginForm, QueryBook, BorrowaBook, AddBook, EditReader,ReturnBook
from .models import User, Book, Reader, Borrowbook
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import time

# Create your views here.
def index(request):
    books = Book.objects.all()
    username=request.session.get("username")
    return render(request,"book/index.html",{"books":books,"username":username})

def login(request):
    if request.method=="POST":
        f=LoginForm(request.POST)
        # print("1:",)

        if f.is_valid():
            user=f.cleaned_data['username']
            passwd=f.cleaned_data['password']
            try:
                user=User.objects.get(name=user)
                if user.password!=passwd:
                    message="密码错误"
                    return render(request,"book/login.html",{"form":f,"message":message})

            except User.DoesNotExist as e:
                message="用户不存在"

                # print(locals)
                return render(request,"book/login.html",{'form':f,"message":message})


            books = Book.objects.all()
            request.session['username'] = user.name
            username=request.session.get("username")
            return render(request,'book/index.html',locals())
        else:
            return render(request, 'book/login.html',locals())
    else:
        f=LoginForm()
        return render(request,"book/login.html",{'form':f})


def queryBook(request):
    if request.method=="POST":
        f = QueryBook(request.POST)
        if f.is_valid():
            bookS = f.cleaned_data['book']
            try:
                a_book=Book.objects.filter(bookname=bookS).values().first()
                ISBN=a_book['ISBN']
                bookname=a_book['bookname']
                author=a_book['author']
                publish=a_book['publish']
                publishDate=a_book['publishdate']
                publishTime=a_book['publishtime']
                unitprice=a_book['unitprice']

                return render(request,"book/queryBook.html",locals())

            except:
                # print("hello")
                message="查无此书"
                return render(request,"book/queryBook.html",{"message":message})
                
    else:
        return render(request, 'book/queryBook.html')


def borrowBook(request):
    if request.method=="GET":
        f=BorrowaBook()
        return render(request, "book/borrowBook.html",{"form":f})
    else:
        breaderid = request.POST.get("readerid")
        # print(type(breaderid)) #str
        obj=Reader.objects.all()
        obj2=obj.get(readerid=breaderid)
        # print(obj2) #Reader object (001)


        bisbn = request.POST.get("isbn")
        b1=Book.objects.all()
        b2=b1.get(ISBN=bisbn)
        borrow_month = request.POST.get("borrowdate_month")
        borrow_day=request.POST.get("borrowdate_day")
        borrow_year=request.POST.get("borrowdate_year")

        borrow_month='{:02}'.format(int(borrow_month))
        borrow_day='{:02}'.format(int(borrow_day))
        borrowdate=borrow_year+"-"+borrow_month+"-"+borrow_day

        returndate_month = request.POST.get("returndate_month")
        returndate_day=request.POST.get("returndate_day")
        returndate_year=request.POST.get("returndate_year")
        returndate_month='{:02}'.format(int(returndate_month))
        returndate_day='{:02}'.format(int(returndate_day))

        returndate=returndate_year+"-"+returndate_month+"-"+returndate_day
        ntime=time.strftime('%Y-%m-%d',time.localtime(time.time()))#获取当前时间   2018-12-02
        def compare_time(time1,time2):
            s_time = time.mktime(time.strptime(time1,'%Y-%m-%d'))
            e_time = time.mktime(time.strptime(time2,'%Y-%m-%d'))
            return int(s_time) - int(e_time)

        result = compare_time(ntime,returndate)
        if result>=0:
            fine=0
        else:
            fine=100
        Bbook=Borrowbook.borrowbook(obj2,b2,borrowdate,returndate,fine)
        Bbook.save()
        # Cannot assign "'001'": "Borrowbook.readerId" must be a "Reader" instance.!!!!!!!
        return HttpResponseRedirect('/index/')

        

def addBook(request):
    if request.method=='GET':
        obj=AddBook()
        return render(request,"book/addbook.html",{"obj":obj})
    else:
        obj=AddBook(request.POST)
        bISBN = request.POST.get("ISBN")
        btypeid = request.POST.get("typeid")
        bbookname=request.POST.get("bookname")
        bauthor=request.POST.get("author")
        bpublish=request.POST.get("publish")
        bpublishdate=request.POST.get("publishdate")
        bpublishtime=request.POST.get("publishtime")
        bunitprice=request.POST.get("unitprice")

        Abook = Book.addbook(bISBN, btypeid, bbookname, bauthor,
        bpublish,bpublishdate,bpublishtime,bunitprice)
        Abook.save()

        return HttpResponseRedirect('/index/')

        

def returnBook(request):
    if request.method=="GET":
        obj=ReturnBook()
        return render(request,"book/returnbook.html",{"obj":obj})
    
    else:
       
        bookid=request.POST.get("bookCode")
        obj=Borrowbook.objects.get(iSBN_id=bookid)
        readerid=request.POST.get("userid")
        if readerid==obj.readerId_id:
            obj.delete()
    return HttpResponse("还书成功")
        # print(obj.fine)

def allbooks(request):
    books=Book.objects.all()
    return render(request,"book/index.html",{"books":books})


def editReader(request,rid):
    if request.method=='GET':
        
        row=Reader.objects.filter(readerid=rid).values("type","name","age","sex","phone","dept","regdate").first()
        obj=EditReader(initial=row)

        return render(request, 'book/editReader.html',{"rid":rid,"obj":obj})
        
    else:   
        obj=EditReader(request.POST)
        if obj.is_valid():
            Reader.objects.filter(readerid=rid).update(**obj.cleaned_data)
            return redirect("/readerlist/")
        return render(request, 'book/editReader.html',{"rid":rid,"obj":obj})


def readerlist(request):
    reader_list=Reader.objects.all()
    return render(request,'book/Readerlist.html',{"readerlist":reader_list})