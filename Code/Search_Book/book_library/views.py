from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import pandas as pd
import numpy
import jieba
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
PATH_DATA=r'C:\Users\R0G\Desktop\1G'

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
                          body=action)
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
            },
            'min_score': 0.000001,
            'explain': True,
            'size': 20
        }
        _searched = self.es.search(
            index=self.index_name,
            body=doc)
        i = 0
        last_author = []
        last_category = []
        last_docxname = []
        last_sentence = []
        last_score = []
        for hit in _searched['hits']['hits']:
            # print(hit['_source'])
            # print ( hit['_source']['title'])
            # print(hit['_score'])
            last_category.append(hit['_source']['category'])
            last_docxname.append(hit['_source']['name'])
            last_author.append(hit['_source']['author_lst'])
            last_sentence.append(hit['_source']['title'])
            last_score.append(hit['_score'])
            i = i + 1
            if i == 200:
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
        print(last_score)
        print(last_score[::-1])
        return last_docxname,last_author,last_sentence, last_score, cost_time
        # print(cost_time)

    def Search_data(self, input_text):
        # doc = {'query': {'match_all': {}}}
        start_time = time()
        doc = {
            "query": {
                "match": {
                    "title": {
                        "query": input_text,

                    }
                }
            },
            #
            'min_score': 0.000001,
            'explain': True,
            'size': 20
        }
        _searched = self.es.search(
            index=self.index_name,
            body=doc)
        i = 0
        last_author = []
        last_category = []
        last_docxname = []
        last_sentence = []
        last_score = []
        for hit in _searched['hits']['hits']:
            # print(hit['_source'])
            # print ( hit['_source']['title'])
            # print(hit['_score'])
            last_category.append(hit['_source']['category'])
            last_docxname.append(hit['_source']['name'])
            last_author.append(hit['_source']['author_lst'])
            last_sentence.append(hit['_source']['title'])
            last_score.append(hit['_score'])
        # print(len(last_sentence))
        #         for temp in last_sentence:
        #             print(temp)
        # print(last_docxname)
        cost_time = time()-start_time
        # print(cost_time)
        print(last_score)
        print(last_score[::-1])
        return last_docxname, last_author, last_sentence,last_score, cost_time

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
            },
            # If there are not setting the sequence, it will return the random some just less 10 results.
            # and we set that search the top 20 score.
            'min_score': 0.000001,
            'explain': True,
            'size': 20
        }
        _searched = self.es.search(
            index=self.index_name,
            body=doc)
        i = 0
        last_author = []
        last_category = []
        last_docxname = []
        last_sentence = []
        last_score = []
        for hit in _searched['hits']['hits']:
            # print(hit['_source'])
            # print ( hit['_source']['title'])
            # print(hit['_score'])
            last_category.append(hit['_source']['category'])
            last_docxname.append(hit['_source']['name'])
            last_author.append(hit['_source']['author_lst'])
            last_sentence.append(hit['_source']['title'])
            last_score.append(hit['_score'])
            i = i + 1
            if i == 200:
                break
        # print(len(last_sentence))
        #         for temp in last_sentence:
        #             print(temp)
        # print(last_docxname)
        cost_time = time()-start_time
        print(last_score)
        print(last_score[::-1])
        return last_docxname, last_author, last_sentence, last_score, cost_time

wy = ElasticWy("4", ip="localhost")
wy.create_index(index_name="4")

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'Home.html')
    if request.method == "POST":
        form1 = request.POST.get("form1")
        form2 = request.POST.get("form2")
        print("===========")
        print(form1, form2)
        # get the first input
        # which search the job with the job name
        res_filename = []
        res_author = []
        res_data = []
        book_info = []
        res_score = []
        if form1!='':
            if form2 == 'Book':
                res_filename,res_author,res_data, res_score, cost_time = wy.Search_name(input_text=form1)
            elif form2 == 'Author':
                res_filename, res_author, res_data,res_score, cost_time = wy.Search_author(input_text=form1)
            # form2 == Word_TFIDF
            else:
                res_filename, res_author, res_data, res_score, cost_time = wy.Search_data(input_text=form1)
            # print(res_filename)
            # print(res_author)
            import numpy as np
            # print(np.unique(res_filename))
            # print(zip(np.unique(res_filename), np.unique(res_author), np.unique(res_data)))
            for i in zip(np.unique(res_filename), np.unique(res_author), np.unique(res_data), res_score):
                book_info.append([i[0],i[1],i[2][200:400], i[3]])
            # print("===========================")
            # print(book_info)
            res_dic = {
                'book_info': book_info,
                'cost_time': cost_time
            }
            return render(request, 'book-list.html', res_dic)
        else:
            result = object.none()

        # for i in result:
        #     print(i.job_id)
        # back to the html
        # return render(request, 'book-list.html', {'result': result})
    return HttpResponse("Connect Successfully!")


def list(request):
    if request.method == 'GET':
        return redirect('/book-list')
    if request.method == "POST":
        form1 = request.POST.get('form1')
        form2 = request.POST.get('form2')
        # get the first input
        # which search the job with the job name
        res_filename = []
        res_author = []
        res_data = []
        book_info = []
        res_score = []
        if form1 != '':
            if form2 == 'Book':
                res_filename, res_author, res_data, res_score, cost_time = wy.Search_name(input_text=form1)
            elif form2 == 'Author':
                res_filename, res_author, res_data, res_score, cost_time = wy.Search_author(input_text=form1)
            # form2 == Word_TFIDF
            else:
                res_filename, res_author, res_data, res_score, cost_time = wy.Search_data(input_text=form1)
            # print(res_filename)
            # print(res_author)
            import numpy as np
            # print(np.unique(res_filename))
            # print(zip(np.unique(res_filename), np.unique(res_author), np.unique(res_data)))
            for i in zip(np.unique(res_filename), np.unique(res_author), np.unique(res_data), np.unique(res_score)):
                book_info.append([i[0], i[1], i[2][200:400], i[3]])
            # print("===========================")
            # print(book_info)
            res_dic = {
                'book_info': book_info,
                'cost_time': cost_time
            }
            return render(request, 'book-list.html', res_dic)
        else:
            result = object.none()

def details(request):
    if request.method == 'GET':
        return redirect('/books-details')

def default(request):
    if request.method == 'GET':
        readfile()
        return redirect('/Home')

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
                            if (every_docx_name!= '' and every_docx_name != None):
                                attribute = every_docx_name.split("_")
                                book_name = attribute[0]
                                print(attribute[1])
                                if len(attribute[1]) <= 4:
                                    author_lst = attribute[1][:-4]
                                else:
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
                            if (every_docx_name != '' and every_docx_name != None):
                                attribute = every_docx_name.split("_")
                                book_name = attribute[0]
                                print(attribute[1])
                                if len(attribute[1]) <= 4:
                                    author_lst = attribute[1]
                                else:
                                    author_lst = attribute[1]
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
