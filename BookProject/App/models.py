from django.db import models

# Create your models here.
class User(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,blank=True)
    password=models.CharField(max_length=20,blank=True)
    class Meta:
            db_table="user"
            ordering=['id']


class Reader(models.Model):
    # Rid=models.ForeignKey("User",on_delete=models.CASCADE)
    readerid=models.CharField(max_length=8,primary_key=True)
    type=models.IntegerField(blank=True)
    name=models.CharField(max_length=20,blank=True)
    age=models.IntegerField(blank=True)
    sex = models.CharField(max_length=4, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    dept = models.CharField(max_length=20, blank=True)
    regdate = models.DateField(blank=True)

    class Meta:
        db_table = "reader"

        # ordering = ['readerid']

class Readertype(models.Model):
    id=models.IntegerField(primary_key=True)
    typename = models.CharField(max_length=20, blank=True)
    maxborrownum = models.IntegerField(blank=True)
    limit = models.IntegerField(blank=True)

    class Meta:
        db_table = "readertype"
        ordering = ['id']

class Book(models.Model):
    # id=models.AutoField()
    ISBN=models.CharField(max_length=10,primary_key=True)
    typeid = models.IntegerField(blank=True)
    bookname = models.CharField(max_length=30,blank=True)
    author = models.CharField(max_length=30, blank=True)
    publish = models.CharField(max_length=30, blank=True)
    publishdate=models.DateField(blank=True) #出版时间
    publishtime=models.IntegerField(blank=True) #印刷次数
    unitprice=models.IntegerField(blank=True)

    class Meta:
        db_table = "book"
        # ordering = ['id']
    
    @classmethod
    def addbook(cls,isbn,tid,bname,bauthor,bpublish,bpublishdate,bpublishtime,bunitprice):
        book=cls(ISBN=isbn,typeid=tid,bookname=bname,
                        author=bauthor,publish=bpublish,publishdate=bpublishdate,
                        publishtime=bpublishtime,unitprice=bunitprice)
        return book
    


class Booktype(models.Model):
    id=models.IntegerField(primary_key=True)
    typename=models.CharField(max_length=30)

    class Meta:
        db_table = "booktype"
        ordering = ['id']


class Borrowbook(models.Model):
    # id = models.IntegerField(primary_key=True)
    readerId = models.ForeignKey(Reader,on_delete=models.CASCADE)
    iSBN = models.ForeignKey(Book,on_delete=models.CASCADE)
    borrowdate = models.DateField(blank=True)
    returndate = models.DateField(blank=True)
    fine = models.IntegerField(blank=True)

    class Meta:
            db_table="borrowbook"
            unique_together=(("readerId","iSBN"),)
            # ordering=['id']

    @classmethod
    def borrowbook(cls,READERID,ISBN,BORROWDATE,RETURNDATE,FINE):
        borrowBook = cls(readerId=READERID, iSBN=ISBN, borrowdate=BORROWDATE,
        returndate=RETURNDATE,fine=FINE
        )
        return borrowBook
