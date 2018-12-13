from django import forms
from django.forms.widgets import SelectDateWidget

class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, required=True,
    error_messages={'required':'用户账号不能为空','invalid':'格式错误'},
    widget=forms.TextInput)

    password = forms.CharField(max_length=16,required=True, 
    error_messages={"required":"密码不能为空"},widget=forms.PasswordInput)

class QueryBook(forms.Form):
    book=forms.CharField(widget=forms.TextInput,required=True)
    

class BorrowaBook(forms.Form):
    readerid=forms.CharField(widget=forms.TextInput,required=True)
    isbn=forms.CharField(widget=forms.TextInput,required=True)
    borrowdate = forms.DateField(widget=SelectDateWidget())
    returndate = forms.DateField(widget=SelectDateWidget())
    
    


class AddBook(forms.Form):
    ISBN=forms.CharField(max_length=10)
    typeid=forms.IntegerField()
    bookname=forms.CharField(max_length=30)
    author=forms.CharField(max_length=30)
    publish=forms.CharField(max_length=30)
    publishdate=forms.DateField()
    publishtime=forms.IntegerField()
    unitprice=forms.IntegerField()

class EditReader(forms.Form):
    type=forms.IntegerField()
    name=forms.CharField(max_length=20)
    age=forms.IntegerField()
    sex=forms.CharField(max_length=4)
    phone=forms.CharField(max_length=11)
    dept=forms.CharField(max_length=20)
    regdate=forms.DateField(disabled=True)#设置标签不可编辑

class ReturnBook(forms.Form):
    bookCode=forms.CharField()
    userid=forms.CharField()
