# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models



class Account(AbstractUser):
    acc_name = models.CharField(max_length=128)
    acc_id = models.IntegerField(null =True)
    acc_type = models.CharField(max_length=30, choices=(('company','company'),('student','student')), default='student')
    state = models.CharField(max_length=30, choices=(('login','login'),('logout','logout')), default='logout')

    def __str__(self):
        return self.acc_name


class CompanyAccount(models.Model):
    Email = models.EmailField(max_length=30, default="123456@qq.com")
    acc_name = models.CharField(max_length=128)
    acc_pwd = models.CharField(max_length=128)
    acc_id = models.IntegerField(primary_key=True)
    account_balance = models.FloatField()

    def __str__(self):
        return self.acc_name


class OrdinaryAccount(models.Model):
    Email = models.EmailField(max_length=30, default="123456@qq.com")
    acc_id = models.IntegerField(primary_key=True)
    acc_name = models.CharField(max_length=50)
    acc_pwd = models.CharField(max_length=128)

    def __str__(self):
        return self.acc_name


class AdjustInfo(models.Model):
    acc = models.OneToOneField(Account, models.DO_NOTHING, primary_key=True)
    administrator = models.ForeignKey('Administrator', models.DO_NOTHING)


class AdjustJobs(models.Model):
    acc = models.ForeignKey('CompanyAccount', models.DO_NOTHING)
    job = models.OneToOneField('Job', models.DO_NOTHING, primary_key=True)


class Administrator(models.Model):
    administrator_id = models.IntegerField(primary_key=True)
    administrator_name = models.CharField(max_length=30)


class Collect(models.Model):
    favorites = models.OneToOneField('Favorites', models.DO_NOTHING, primary_key=True)
    acc = models.ForeignKey('OrdinaryAccount', models.DO_NOTHING)
    url = models.CharField(db_column='URL', max_length=100)  # Field name made lowercase.


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    def __str__(self):
        return self.company_name


class Favorites(models.Model):
    favorites_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=50)
    job_name = models.CharField(max_length=30)
    url = models.CharField(db_column='URL', max_length=100)  # Field name made lowercase.


class History(models.Model):
    history = models.OneToOneField('HistoryRecord', models.DO_NOTHING, primary_key=True)
    acc = models.ForeignKey('OrdinaryAccount', models.DO_NOTHING)


class HistoryRecord(models.Model):
    history_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=50)
    job_name = models.CharField(max_length=30)
    url = models.CharField(db_column='URL', max_length=100)  # Field name made lowercase.


class Job(models.Model):
    job_id = models.IntegerField(primary_key=True)
    job_name = models.CharField(max_length=100)
    salary = models.FloatField()
    label = models.CharField(max_length=100)
    class_id = models.IntegerField()
    detail_url = models.CharField(db_column='detail_URL', max_length=105, blank=True, null=True)  # Field name made lowercase.
    company_id = models.IntegerField(null = True)
    def __str__(self):
        return self.job_name



class Recharge(models.Model):
    recharge_list = models.OneToOneField('RechargeInfo', models.DO_NOTHING, db_column='recharge_list', primary_key=True)
    acc_id = models.ForeignKey(CompanyAccount, models.DO_NOTHING)

    def __str__(self):
        return self.acc_id


class RechargeInfo(models.Model):
    recharge_list = models.IntegerField(primary_key=True)
    recharge_amount = models.FloatField()
    recharge_time = models.DateField()
    def __str__(self):
        return self.recharge_list


class Requirement(models.Model):
    job_id = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    experiance = models.CharField(max_length=30, blank=True, null=True)
    degree = models.CharField(max_length=30, blank=True, null=True)
    def __str__(self):
        return self.job_id


class Search(models.Model):
    job = models.OneToOneField(Job, models.DO_NOTHING, primary_key=True)
    acc = models.ForeignKey(OrdinaryAccount, models.DO_NOTHING)



class ViewInfo(models.Model):
    acc = models.ForeignKey(CompanyAccount, models.DO_NOTHING)
    company = models.OneToOneField(Company, models.DO_NOTHING, primary_key=True)
