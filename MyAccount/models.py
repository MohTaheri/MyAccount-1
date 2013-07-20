__author__ = 'arash'
from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class User(models.Model):
   userName = models.CharField(max_length=20,unique=True)
   # needs to be changed !
   password = models.CharField(max_length=128)
   name = models.CharField(max_length=20)
   familyName = models.CharField(max_length=20)
   khomstalab = models.BooleanField()
   teammates = models.ManyToManyField('User',through='Cohort')

   def __unicode__(self):
       return self.userName

class Cohort(models.Model):
    idUser1 = models.ForeignKey(User,related_name='peopleThatAreMyTeammate')
    idUser2 = models.ForeignKey(User,related_name='peopleThatImTheirTeammate')
    budgetPermission = models.BooleanField()
    class Meta:
        unique_together = ("idUser1","idUser2")

    def __unicode__(self):
        return self.idUser1.userName + " , " + self.idUser2.userName


class khoms(models.Model):
    userid = models.ForeignKey(User)
    year = models.IntegerField()
    amount = models.IntegerField()

    def __unicode__(self):
        return self.userid + " in year " + self.year


class Bank(models.Model):
    userid = models.ForeignKey(User,related_name="banks")
    name = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)
    description = models.CharField(max_length=400,blank=True)
    class Meta:
        unique_together =("userid","name","branch")

class Account(models.Model):
    userid = models.ForeignKey(User,related_name="accounts")
    name = models.CharField(max_length=100)
    balance = models.IntegerField()
    transferAccounts = models.ManyToManyField('Account',through='AccountTransfer')
    def __unicode__(self):
        return self.name

class BankAccount(Account):
    accountNumber=models.CharField(max_length=20)
    correspondingBank = models.ForeignKey(Bank)


class AccountTransfer(models.Model):
    fromAccount = models.ForeignKey(Account,related_name="AccountsTransferedTo")
    toAccount = models.ForeignKey(Account,related_name="AccountsTransferedFrom")
    amount = models.IntegerField()
    transferTime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=400,blank=True)
    def __unicode__(self):
        return "from account  " + self.fromAccount.name + "to account  " + self.toAccount.name


class IncomeType(models.Model):
    userid = models.ForeignKey(User,related_name="IncomeTypes")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400,blank=True)
    class Meta:
        unique_together = ("userid","title")
    def __unicode__(self):
        return self.title


class ExpenseType(models.Model):
    userid = models.ForeignKey(User,related_name="ExpenseTypes")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400,blank=True)
    budget = models.IntegerField(blank=True,null=True)
    class Meta:
        unique_together = ("userid","title")
    def __unicode__(self):
        return self.title

class Notification(models.Model):
    userid = models.ForeignKey(User,related_name="notifs")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title

class Memo(models.Model):
    userid = models.ForeignKey(User,related_name="Memos")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=400,blank=True)
    creationTime = models.DateTimeField(auto_now=True)
    reminder = models.BooleanField(default=False)
    startTime = models.DateTimeField(blank=True,null=True)
    endTime = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=20)
    def __unicode__(self):
        return self.title

class Merchant(models.Model):
    name = models.CharField(max_length=20)
    expenseType = models.ForeignKey(ExpenseType,blank=True,null=True)
    incomeType = models.ForeignKey(IncomeType,blank=True,null=True)
    description = models.CharField(max_length=400,blank=True)

class Transaction(models.Model):
    userid = models.ForeignKey(User,related_name="Transactions")
    title = models.CharField(max_length=100)
    creationTime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=400,blank=True)
    merchant = models.ForeignKey(Merchant,blank=True,null=True)
    amount = models.IntegerField()
    correspondigAccount = models.ForeignKey(Account)

class Expense(Transaction):
    time = models.DateTimeField()
    type = models.ForeignKey(ExpenseType)

class creditDebt(Transaction):
    status = models.CharField(max_length=20)
    debtDue = models.DateTimeField(blank=True,null=True)
    creditOrDebt = models.BooleanField()


class Income(Transaction):
    type = models.ForeignKey(IncomeType)
    time = models.DateTimeField(blank=True,null=True)

class Cheque(Transaction):
    serial= models.CharField(max_length=16,unique=True)
    creditOrDebt = models.BooleanField()
    status = models.CharField(max_length=20)
    picturePath = models.ImageField(upload_to="/checkImages",max_length=100,blank=True)
    issueDate = models.DateField()
    drawee = models.ForeignKey(Bank)

class Loan(Transaction):
    status = models.CharField(max_length=20)
    repaymentDate = models.DateField()
    bank = models.ForeignKey(Bank)

