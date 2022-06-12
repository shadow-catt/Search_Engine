import math

import pymysql
import sqlalchemy
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators import csrf
import random
import  time
from django.contrib import auth
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# from . import models
# from .form import LoginForm
# from .models import Account, CompanyAccount, OrdinaryAccount, Company, Job, AdjustJobs
from django.contrib.auth.decorators import login_required
# 在类之前需要添加以下两行代码
from django.utils.decorators import method_decorator

# 主要执行函数
'''将docx转化为txt'''


import pandas as pd
import numpy
import jieba
import os
from threading import Thread
import time
from os import walk
#import CSVOP
import codecs
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from time import time
import os
import sys
import fnmatch
import win32com.client

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
#print(PATH)
PATH_DATA=r'E:\Desktop_xsj\Desktop\Workshop\1G'

def docx_to_text():
    wordapp = win32com.client. \
        gencache.EnsureDispatch("Word.Application")
    try:
        for root, dirs, files \
                in os.walk(PATH_DATA):
            # root代表路径,dirs代表目录，files代表文件名
            print(root, dirs, files)
            for _dir in dirs:  # 若是目录，跳过
                pass
            for _file in files:  # 若是文件，转化为txt
                if not fnmatch. \
                        fnmatch(_file, '*.docx'):
                    # 若是docx结尾，才进行操作
                    continue
                word_file = os.path.join(root, _file)
                wordapp.Documents.Open(word_file)
                # 打开word文件
                docastxt = word_file[:-4] + 'txt'
                # 新建txt的文件名
                wordapp.ActiveDocument \
                    .SaveAs(
                    docastxt,
                    FileFormat=
                    win32com.client.constants.wdFormatText)
                wordapp.ActiveDocument.Close()
    finally:
        wordapp.Quit()
    print("well done!")


'''遍历TXT文件并且调用es插入数据'''


def readfile():
    docx_name = []  # 存储文件名
    filename = []  # 存储文件种类名
    all_file = []  # 存储所有文件
    # temp1=[]
    content = []
    print('文件开始读取')
    x = -1
    try:
        for root, dirs, files in os.walk(PATH_DATA):
            # print(x)
            if x == -1:
                # print(dirs)
                for name in dirs:  # 访问第一层文件夹
                    # print(name)
                    filename.append(name)
                    temp_content = []
            else:
                # print(files)
                # temp=[]
                # print('已经读取到', filename[x], '文件夹')
                cishu = 1
                temp_content = []
                for every_docx_name in files:
                    # print('hang',hang)
                    every_file_path = \
                        os.path.join(root, every_docx_name)
                    # print(every_file_path)
                    # print(every_file_path)
                    # print(filename)
                    try:  # 判断编码问题
                        with codecs.open(every_file_path,
                                         encoding='utf-8') as f:
                            temp = f.read()
                            # print('++++',temp)
                            '''输出各个文档的信息'''
                            # print('name', filename[x],
                            #       'docname', every_docx_name,
                            #       'content', len(temp))
                            '''执行文档插入操作'''
                            # print('gbk: ' + every_docx_name)
                            # print("===================")
                            attribute = every_docx_name.split("_")
                            book_name = attribute[0]
                            author_lst = attribute[1][:-4]
                            # print("===================")
                            # print(author_lst)
                            wy.Index_Data \
                                (filename[x],
                                 book_name,
                                 author_lst,
                                 temp,
                                 cishu)
                        cishu = cishu + 1

                    except UnicodeDecodeError:
                        # 如果不是gbk，执行utf-8操作
                        with codecs.open(every_file_path,
                                         encoding='gbk') as f:
                            temp = f.read()
                            # print('++++',temp)
                            # print('name', filename[x],
                            #       'docname', every_docx_name,
                            #       'content', len(temp))
                            # ''''''
                            '''执行文档插入操作'''
                            print('utf-8: ' + every_docx_name)
                            attribute = every_docx_name.split("_")
                            book_name = attribute[0]
                            author_lst = attribute[1][:-4]
                            # print("===================")
                            # print(author_lst)
                            wy.Index_Data \
                                (filename[x],
                                 book_name,
                                 author_lst,
                                 temp,
                                 cishu)
                            cishu = cishu + 1

                    # temp_content.append(temp)
                # print(len(temp_content))
                # content.append(temp_content)
                # print(every_file_path)

            x = x + 1

            # print(files)


    finally:
        print("文件读取完成")
        # return filename,all_file,docx_name


'''文件操作结束，开始es'''
'''文件操作结束，开始es'''
'''文件操作结束，开始es'''


class ElasticWy:
    def __init__(self, index_name, ip="localhost"):

        self.index_name = index_name
        self.es = Elasticsearch([ip], port=9200)

    def create_index(self, index_name):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        # 创建映射
        _index_mappings = {
            "mappings": {
                #                 self.index_type: {
                "properties": {
                    "source": {
                        "type": "text",
                        "index": True,
                        # "author": "ik_max_word",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                }
                #                 }
            }
        }
        if self.es.indices.exists \
                    (index=self.index_name) is not True:
            res = self.es.indices.create \
                (index=self.index_name, body=_index_mappings)
            print('1', res)

    def ReadFile(self, filepath):
        # filepath='C:\\Users\\wy\\Desktop\\data' \
        #          '\\elasticsearch\\data.txt'
        if os.path.exists(filepath) and os.path.isfile(filepath):
            print("*********文件成功读取完毕*********")
            with open(filepath) as f:
                temp_list = []
                for line in f:
                    temp_set = {}
                    # print(line)
                    temp_set = str(line)
                    temp_list.append(temp_set)
                # print(temp_list)
            return temp_list
        else:
            print("错误：文件目录不存在或文件不存在")

    def Index_Data(self, category, book_name, author_lst, content, cishu):

        if isinstance(content, str):  # 判断是否为表类型
            # print('插入数据')
            # for category,name,line in namelist,docname,filelist:

            action = {
                'category': category,
                'name': book_name,
                'author_lst': author_lst,
                "title": content}
            # ACTIONS.append(action)
            self.es.index(index=self.index_name,
                          body=action//)
            print('已经插入', cishu, '条记录')
        else:
            print("错误：文件尚未成功从目录中写入库")

    def Search_name(self, input_text):
        # doc = {'query': {'match_all': {}}}
        start_time = time()
        doc = {
            "query": {
                "match": {
                    "name": {
                        "query": input_text,
                        "operator": "and"
                    }
                }
            }
        }
        _searched = self.es.search(
            index=self.index_name,
            body=doc)
        i = 0
        last_author = []
        last_category = []
        last_docxname = []
        last_sentence = []
        for hit in _searched['hits']['hits']:
            # print(hit['_source'])
            # print ( hit['_source']['title'])
            # print(hit['_score'])
            #             print(hit)
            last_category.append(hit['_source']['category'])
            last_docxname.append(hit['_source']['name'])
            last_author.append(hit['_source']['author_lst'])
            last_sentence.append(hit['_source']['title'])

            i = i + 1
            if i == 20:
                break
        # print(len(last_sentence))
        #         for temp in last_sentence:
        #             print(temp)
        #         print(last_category)
        #         print("=============")
        #         print(last_sentence)
        #         print("=============")
        # print(last_docxname)
        # print("=============")
        # print(last_author)
        cost_time = time()-start_time
        return last_docxname,last_author,last_sentence,cost_time
        # print(cost_time)

    def Search_data(self, input_text):
        # doc = {'query': {'match_all': {}}}
        start_time = time()
        doc = {
            "query": {
                "match": {
                    "title": {
                        "query": input_text,
                        "operator": "and"
                    }
                }
            }
        }
        _searched = self.es.search(
            index=self.index_name,
            body=doc)
        i = 0
        last_author = []
        last_category = []
        last_docxname = []
        last_sentence = []
        for hit in _searched['hits']['hits']:
            # print(hit['_source'])
            # print ( hit['_source']['title'])
            # print(hit['_score'])
            last_category.append(hit['_source']['category'])
            last_docxname.append(hit['_source']['name'])
            last_author.append(hit['_source']['author_lst'])
            last_sentence.append(hit['_source']['title'])
            i = i + 1
            if i == 20:
                break
        # print(len(last_sentence))
        #         for temp in last_sentence:
        #             print(temp)
        # print(last_docxname)
        cost_time = time()-start_time
        # print(cost_time)
        return last_docxname, last_author, last_sentence, cost_time

    def Search_author(self, input_text):
        # doc = {'query': {'match_all': {}}}
        start_time = time()
        doc = {
            "query": {
                "match": {
                    "author_lst": {
                        "query": input_text,
                        "operator": "and"
                    }
                }
            }
        }
        _searched = self.es.search(
            index=self.index_name,
            body=doc)
        i = 0
        last_author = []
        last_category = []
        last_docxname = []
        last_sentence = []
        for hit in _searched['hits']['hits']:
            # print(hit['_source'])
            # print ( hit['_source']['title'])
            # print(hit['_score'])
            last_category.append(hit['_source']['category'])
            last_docxname.append(hit['_source']['name'])
            last_author.append(hit['_source']['author_lst'])
            last_sentence.append(hit['_source']['title'])
            i = i + 1
            if i == 20:
                break
        # print(len(last_sentence))
        #         for temp in last_sentence:
        #             print(temp)
        # print(last_docxname)
        cost_time = time()-start_time
        # # print(cost_time)
        return last_docxname, last_author, last_sentence, cost_time

wy = ElasticWy("4", ip="localhost")
wy.create_index(index_name="4")
readfile()
# # return filename, all_file, docx_name
# # docname=readfile()[2]
# # filelist=readfile()[1]
# # namelist=readfile()[0]


# @login_required(login_url= 'login')
# def index(request):
#     if request.method == 'GET':
#         return render(request, 'index.html')
#     if request.method == "POST":
#         form1 = request.POST.get('form1')
#         form2 = request.POST.get('form2')
#         # get the first input
#         # which search the job with the job name
#         if form1!='':
#             find1 = Job.objects.filter(job_name__contains=form1)
#             result1 = find1
#         # get the first input
#         # which search the job with the job name
#         if form2 != '':
#             find3comid = Company.objects.filter(city__icontains=form2).values('company_id')
#             find3 = Job.objects.filter(company_id__in=find3comid)
#             result2 = find3
#
#         # if user input the the both search box
#         if form1!='' and form2!='':
#             # join the result of querySet
#             result = result1 & result2
#         elif form1!='':
#             result = result1
#         elif form2!='':
#             result = result2
#         else:
#             result = object.none()
#         # for i in result:
#         #     print(i.job_id)
#         # back to the html
#         return render(request, 'findJob.html', {'result': result})
#
#
# # @login_required(login_url= 'login')
# def profile(request):
#     cid = 0
#     if request.method == 'GET':
#         cid = request.GET.get('jid')
#         print(cid)
#
#         # update the company and companyAccount information
#         company = Company.objects.get(company_id=cid)
#         comAcc = CompanyAccount.objects.get(acc_id=cid)
#         print(company.company_name)
#         name = company.company_name
#         id = company.company_id
#         address = company.city
#         email = comAcc.Email
#         return render(request, 'profile.html', {'name': name, 'id':id, 'address':address, 'email': email})
#
#     if request.method == 'POST':
#         # get all information the user input
#         cid =  request.GET.get('jid')
#         newEmail = request.POST.get('email')
#         newName = request.POST.get('name')
#         newCity = request.POST.get('address')
#         newC = Company.objects.filter(company_id=cid).update(company_name=newName, city=newCity)
#         newA = CompanyAccount.objects.filter(acc_id=cid).update(Email=newEmail)
#         return redirect('/uicjob/indexCompany')
#
# # visualization part
# def visualization(request):
#     return render(request, 'visualization.html')
#
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     print(request.method)
#     if request.method == "POST":
#         superusers_name = Account.objects.filter(is_superuser=True).values_list('username')
#         notsuper_name = Account.objects.filter(is_superuser=False).values_list('username')
#         # print(superusers_name)
#         # print(notsuper_name)
#         username = request.POST.get('username', None)
#         password = request.POST.get('pwd', None)
#         message = "PLease enter your information (^-^)"
#         if username and password:  # make sure the password and username is not empty
#             dete1 = False
#             for i in notsuper_name:
#                 if username in i:
#                     dete1 = True
#             if dete1 == True:
#                 # make sure the password is correct
#                 acc = auth.authenticate(request, username=username, password=password)
#                 if acc:
#                     # we have two types of account: student and company
#                     if acc.is_active:
#                         if acc.acc_type == 'student':
#                             auth_login(request, acc)
#                             return redirect('/uicjob/index')
#                         if acc.acc_type == 'company':
#                             auth_login(request, acc)
#                             return redirect('/uicjob/indexCompany')
#                     else:
#                         message = "Account is freeze!"
#                 else:
#                     message = "Incorrect password!"
#
#             dete2 = False
#             # if the username and password accord with the superuser
#             for i in superusers_name:
#                 if username in i:
#                     dete2 = True
#             if dete2 == True:
#                 user = authenticate(request, username=username, password=password)
#                 if user:
#                     if user.is_active:
#                         #  redirect to the admin interface
#                         return redirect('http://127.0.0.1:8000/admin')
#                     else:
#                         message = "Account is freeze!"
#                 if user == None:
#                     message = "Incorrect password!"
#             if dete2 == False and dete1 ==False:
#                 message = "The username does not exist!"
#         # Turn back  the all error messages
#         return render(request, 'login.html', {"message": message})
#
#
# def register(request):
#     # comList = Company.objects.values("company_id", "company_name", "city")[:]
#     # for i in comList:
#         # print(i.get('company_id'))
#         # newC = Account.objects.filter(acc_name=i.get('company_name')+str(i.get('company_id')+1)).delete()
#         # newA = Account.objects.create(acc_name=i.get('company_name')+str(i.get('company_id')+1), username=(i.get('company_name')+str(i.get('company_id')+1)), acc_id=i.get('company_id'), password=make_password('123456'), acc_type='company')
#         # newA.save()
#     superusers_name = Account.objects.filter(is_superuser=True).values_list('username')
#     if request.method == 'GET':
#         return render(request, 'register.html')
#     if request.method == 'POST':
#         # register
#         name = request.POST.get('username')
#         password = request.POST.get('password')
#         pwd_corr = request.POST.get('pwd_corr')
#         email  = request.POST.get('email')
#         choice = request.POST.get('type')
#         message = "Please complete your information! (^_^)"
#         print(name, password, pwd_corr, email, choice)
#         if email and password and pwd_corr and name and choice:
#             try:
#                 acc = Account.objects.get(username=name)
#                 message = 'The user already exists!'
#             except:
#                 dete = False
#                 for i in superusers_name:
#                     if name in i:
#                         dete = True
#                 if dete == True:
#                     message = "The user already exists!"
#                 if dete == False:
#                     if pwd_corr != password:
#                         message = 'The two passwords entered are inconsistent!'
#                     if pwd_corr == password:
#                         password = make_password(password)
#                         id = ''
#                         if choice == 'company':
#                             id = int(max(CompanyAccount.objects.values_list("acc_id"))[0])+1
#                             newcompany = CompanyAccount.objects.create(acc_id=id, acc_name=name, acc_pwd=password, Email=email, account_balance=0)
#                             newcomAcc = Company.objects.create(company_id=id, company_name=name+str(id), city='China')
#                             newcompany.save()
#                         if choice == 'student':
#                             id = int(max(OrdinaryAccount.objects.values_list("acc_id"))[0])+1
#                             newstudent = OrdinaryAccount.objects.create(acc_id=id, acc_name=name, acc_pwd=password, Email=email)
#                             newstudent.save()
#
#                         newaccount = Account.objects.create(acc_id=id, username=name, password=password, acc_type=choice, email = email, state='logout')
#                         newaccount.save()
#                         print(password)
#                         return redirect('/uicjob/login')
#         return render(request, 'register.html', {"message": message})


def book_search(request):
    if request.method == 'GET':
        print("xxxxxxxxxxxx")
        return render(request, 'Home.html')
    # if request.method == "POST":
    #     form1 = request.POST["form1"]
    #     form2 = request.POST.get("form2")
    #     print("=========")
    #     print(form1, form2)
    #     # get the first input
    #     # which search the job with the job name
    #     res_filename = []
    #     res_author = []
    #     res_data = []
    #     book_info = []
    #     if form1!='':
    #         if form2 == 'Title':
    #             res_filename,res_author,res_data,cost_time = wy.Search_name(input_text=form1)
    #         elif form2 == 'Author':
    #             res_filename, res_author, res_data,cost_time = wy.Search_author(input_text=form1)
    #         # form2 == Word_TFIDF
    #         else:
    #             res_filename, res_author, res_data,cost_time = wy.Search_data(input_text=form1)
    #
    #         for i in zip(list(set(res_filename)), list(set(res_author))):
    #             book_info.append([i[0],i[1]])
    #         print("===========================")
    #         print(book_info)
    #         res_dic = {
    #             'book_info': (book_info),
    #             'cost_time':cost_time
    #         }
    #         return render(request, 'book_list.html', res_dic)
    #     else:
    #         result = object.none()
    #
    #     # for i in result:
    #     #     print(i.job_id)
    #     # back to the html
    #     return render(request, 'book_list.html', {'result': result})
    # return HttpResponse("Connect Successfully!")

def success(request):
    return redirect('/uiclibrary/Home')
    # return HttpResponse("Connect Successfully!")

def book_list(request):
    if request.method == 'GET':
        return redirect('/uiclibrary/book-list')
    # if request.method == "POST":
    #     form1 = request.POST.get('form1')
    #     form2 = request.POST.get('form2')
    #     # get the first input
    #     # which search the job with the job name
    #     res_filename = []
    #     res_author = []
    #     res_data = []
    #     book_info = []
    #     if form1 != '':
    #         if form2 == 'Title':
    #             res_filename, res_author, res_data, cost_time = wy.Search_name(input_text=form1)
    #         elif form2 == 'Author':
    #             res_filename, res_author, res_data, cost_time = wy.Search_author(input_text=form1)
    #         # form2 == Word_TFIDF
    #         else:
    #             res_filename, res_author, res_data, cost_time = wy.Search_data(input_text=form1)
    #
    #         for i in zip(list(set(res_filename)), list(set(res_author))):
    #             book_info.append([i[0], i[1]])
    #         print("===========================")
    #         print(book_info)
    #         res_dic = {
    #             'book_info': (book_info),
    #             'cost_time': cost_time
    #         }
    #         return render(request, 'book_list.html', res_dic)
    #     else:
    #         result = object.none()
    #
    #     # for i in result:
    #     #     print(i.job_id)
    #     # back to the html
    #     return render(request, 'book_list.html', {'result': result})
    # return HttpResponse("Connect Successfully!")


def book_detail(request):
    if request.method == 'GET':
        return redirect('/uiclibrary/books-details')


#
# # In the findJOb interface, we can also search the company job and city
# def findJob(request):
#     if request.method == 'GET':
#         return redirect('/uicjob/findJob')
#     if request.method == "POST":
#         form1 = request.POST.get('form1')
#         form2 = request.POST.get('form2')
#
#         if form1 != '':
#             find1 = Job.objects.filter(job_name__contains=form1)
#             # result1 = find1 | find2
#             result1 = find1
#         if form2 != '':
#             find3comid = Company.objects.filter(city__icontains=form2).values('company_id')
#             find3 = Job.objects.filter(company_id__in=find3comid)
#             result2 = find3
#
#         if form1 != '' and form2 != '':
#             result = result1 & result2
#         elif form1 != '':
#             result = result1
#         elif form2 != '':
#             result = result2
#         else:
#             result = object.none()
#
#         # redirect('/uicjob/findJob')
#         return render(request, 'findJob.html', {'result': result})
#
#
# @login_required(login_url= 'login')
# def indexCompany(request):
#     id = request.user.acc_id
#     print(id)
#
#     findJ = Job.objects.filter(company_id=int(id))
#     start = time.time()
#     lstlst=[]
#     for i in findJ:
#         lst = []
#         lst.append((i.job_id))
#         lst.append(i.job_name)
#         if i.class_id == 0:
#             lst.append('Java')
#         elif i.class_id == 1:
#             lst.append('Python')
#         elif i.class_id == 2:
#             lst.append('C++')
#         elif i.class_id == 3:
#             lst.append('Php')
#         else:
#             lst.append('Others')
#         lst.append(i.detail_url)
#         lst.append(i.salary)
#         lstlst.append(lst)
#     end = time.time()
#
#     print(end-start)
#     runtime = end-start
#     num = request.GET.get('num', 1)
#     n = int(num)
#     # search all job
#     accounts = Account.objects.all()
#
#     # Create the pager object
#     pager = Paginator(accounts, 20)
#
#     # Gets the data for the current page
#     try:
#         curr_page_data = pager.page(n)
#     except PageNotAnInteger:
#         # Returns the data on the first page
#         curr_page_data = pager.page(1)
#     except EmptyPage:
#         # Returns the data on the last page
#         curr_page_data = pager.page(pager.num_pages)  # num_pages 总页数
#
#     # round fluctuation page
#     # Start page number of each page
#     begin = (n - int(math.ceil(10.0 / 2)))
#     if begin < 1:
#         begin = 1
#
#     # Start page number of each page
#     end = begin + 9
#     if end > pager.num_pages:
#         end = pager.num_pages
#
#     if end <= 10:
#         begin = 1
#     else:
#         begin = end - 9
#
#     page_list = range(begin, end + 1)
#     dic = {'time': runtime, 'job': lstlst, 'pager': pager, 'curr_page_data': curr_page_data, 'page_list': page_list}
#     return render(request, 'indexCompany.html', dic)
#
# def logout(request):
#     return redirect('login')
#
#
# @login_required(login_url= 'login')
# def deleteJob(request):
#     jid = request.GET.get('jid')
#     print(jid)
#     deleJ = Job.objects.filter(job_id=jid).delete()
#     return redirect('/uicjob/indexCompany')
#
# @login_required(login_url= 'login')
# def changeJob(request):
#     if request.method == 'GET':a
#         jid = request.GET.get('jid')
#         change = Job.objects.get(job_id=jid)
#         print(type(change.label))
#         print(len(change.label))
#         if change.label == '[]':
#             change.label = 'There are not some details'
#         dic = {
#             'jname': change.job_name,
#             'jsalary': change.salary,
#             'jlabel': change.label
#         }
#         return render(request, 'changeJob.html', dic)
#
#     if request.method == 'POST':
#         jid = request.GET.get('jid')
#         newName = request.POST.get('jname')
#         newSalary = request.POST.get('jsalary')
#         newLabel = request.POST.get('jlabel')
#         newKind = request.POST.get('type')
#         print(newSalary,newKind,newName,newLabel)
#         change = Job.objects.filter(job_id=jid).update(label=newLabel,job_name=newName,class_id=newKind,salary=newSalary)
#         return redirect('/uicjob/indexCompany')
#
#
# @login_required(login_url= 'login')
# def addJob(request):
#     if request.method == 'GET':
#         cid = request.GET.get('jid')
#         return render(request, 'addJob.html')
#     if request.method == 'POST':
#         cid = request.GET.get('jid')
#         print(cid)
#         findJ = Job.objects.filter(company_id=cid)
#         lens = len(findJ)
#         print(lens)
#
#         newName = request.POST.get('jname')
#         newSalary = request.POST.get('jsalary')
#         newLabel = request.POST.get('jlabel')
#         newKind = request.POST.get('type')
#         print(newSalary, newKind, newLabel, newName)
#         if lens == 0:
#             id = int('1001' + str(cid))
#         else:
#             lst = []
#             for i in findJ:
#                 string = str(i.job_id)
#                 string = string[0:4]
#                 lst.append(int(string))
#             # print(lst)
#             maxid = max(lst) + 1
#             print(maxid)
#             id = int(str(maxid) + str(cid))
#         print(id)
#         newJ = Job.objects.create(company_id = cid, label=newLabel,job_name=newName,class_id=newKind,salary=newSalary, job_id=id)
#         return redirect('/uicjob/indexCompany')
#
#
# def studentInfo(request):
#     if request.method == 'GET':
#         username=request.user.username
#         print(username)
#         student = Account.objects.get(username=username)
#         print(student.username)
#         name = student.username
#         id = student.acc_id
#         email = student.email
#         return render(request, 'studentInfo.html', {'name': name, 'id':id, 'email': email})
#
#     if request.method == 'POST':
#         username = request.user.username
#         newEmail = request.POST.get('email')
#         newName = request.POST.get('name')
#         print(newName)
#         newS = OrdinaryAccount.objects.filter(acc_name=username).update(Email=newEmail, acc_name=newName)
#         newA = Account.objects.filter(username=username).update(email=newEmail, username=newName, acc_name = newName)
#
#         # print(company.acc_name)
#         return redirect('/uicjob/index')
#
#
#
#
