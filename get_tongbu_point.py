# coding: utf-8

from db import db_session
from models import *
import random
from bs4 import BeautifulSoup
import requests
# import urllib2
import urllib
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")

__author__ = 'think'


# 同步知识点比较复杂，同步知识点要分为教材版本和教材类型，比如说人教版必修1，每个知识点后面还要加上章节，比如第一章，第一小节。
# 同步知识点编号前面有tb两个字符，后面是“高中”或者“初中”的简称，然是是科目的简称，然后是一二三级编号。有同步知识点的科目如下：

# id_format = {'gzyuwen': u'高中语文', 'gzshuxue': u'高中数学', 'gzyingyu': u'高中英语', 'gzhuaxue': u'高中化学', 'gzwuli': u'高中物理',
#              'gzshengwu': u'高中生物', 'gzlishi': u'高中历史', 'gzdili': u'高中地理', 'gzzhengzhi': u'高中政治',
#              'tbyw': u'初中语文', 'tbsx': u'初中数学', 'tbyy': u'初中英语', 'tbwl': u'初中物理', 'tbhx': u'初中化学', 'tbsw': u'初中生物',
#              'tbls': u'初中历史', 'tbdl': u'初中地理', 'tbzz': u'初中政治'}
id_format = {
    'gzshuxue': u'高中数学', 'gzyingyu': u'高中英语', 'gzhuaxue': u'高中化学', 'gzwuli': u'高中物理', 'gzshengwu': u'高中生物',
    'tbyw': u'初中语文', 'tbyy': u'初中英语','tbls': u'初中历史', 'tbdl': u'初中地理', 'tbzz': u'初中政治'
}
base_url = 'http://www.yitiku.cn/tiku/'


def get_tb_point():
    """
    抓取同步知识点流程：首先获取教材的类型，然后按照教材的版本获取教材的版本，然后抓取
    每个教材的章节知识点,教材编号和知识点编号用原来的编号。
    :return:
    """
    for km in id_format:
        f = open('finish.txt', 'a+')  # 记录开始进度
        f.write('begin:  ' + km + '\n')
        f.close()
        get_book_type(km)


def get_book_type(para_km):
    """
    得到一个科目编号，比如gzyuwen，然后取寻找每个教材类型的url，然后根据该url抓取知识点
    :param para_km:
    :return:
    """
    main_page_url = base_url + para_km + '/'
    content = urllib.urlopen(main_page_url)
    print content.code
    quest_soup = BeautifulSoup(content, 'lxml')  # 整个页面的内容

    book_version_dl = quest_soup.find('dl', class_='bbxz')  # 教材的版本放在dl标签里面
    book_version_dd = book_version_dl.find('dd')  # 教材的版本放在dl标签里面的dd标签里
    book_version_a_list = book_version_dd.find_all('a')  # 教材的版本放在dl标签里面的dd标签里的a标签里
    # book_version_a_list_len = len(book_version_a_list)
    # if book_version_a_list_len == 0:
    #     continue
    for num_a in book_version_a_list:
        b_version = num_a.text  # 获取教程的类型，如人教版
        b_version_href = num_a['href']  # 这个是教程版本的编号,样例"/tiku/gzdili/banben/5984"
        b_version_id =  b_version_href.split('/')[4]
        b_version_url = main_page_url + 'banben' + '/' + b_version_id  # 这个是每个版本教材的主地址,里面有类似于“必修1”这样的教材类型
        content = urllib.urlopen(b_version_url)
        print content.code
        quest_soup = BeautifulSoup(content, 'lxml')  # 整个页面的内容
        b_type_dl = quest_soup.find('dl', class_='bbxz mb5')  # 获取教材的类型,在一个dl标签里面
        b_type_dd = b_type_dl.find('dd')
        b_type_a_list = b_type_dl.find_all('a')
        # b_type_a_list_len = len(b_type_a_list)
        print b_type_a_list
        for each_a in b_type_a_list:  # 每个a标签：<a class="on" href="/tiku/gzdili/jid/12201">必修一</a>
            print each_a
            b_type_name = each_a.text
            b_type_href = each_a['href']
            b_type_href_split = b_type_href.split('/')
            b_type_href_len = len(b_type_href_split)
            b_type_id = b_type_href_split[b_type_href_len-1]
            b_finial_url = b_version_url + '/' + 'jid/' + b_type_id

            para = [b_finial_url, b_version, b_type_name, b_type_id, para_km, b_version_id]
            begin_find(para)

            f = open('finish.txt', 'a+')  # 记录结束进度
            f.write('end:  ' + b_type_name + '\n')
            f.close()

            time.sleep(15)


def begin_find(pare_list):
    """
    参数list含义[每个教材类型的url，教材的版本，教材的类型，教材的编号]
    根据上面的信息抓取知识点
    :param pare_list:
    :return:
    """
    in_url = pare_list[0]
    subj = pare_list[4]

    print in_url
    content = urllib.urlopen(in_url)
    quest_soup = BeautifulSoup(content, 'lxml')  # 整个页面的内容
    point_ul = quest_soup.find('ul', id='root')
    all_point_list = point_ul.find_all('li', recursive=False)  # 抓取所有知识点的li标签
    point_len = len(all_point_list)  # 获取所有一级知识点的个数
    for i in range(point_len):
        first_a = all_point_list[i].find('label').find('a')
        each_first_point = first_a.text  # 一级知识点的名称
        first_a_href = first_a['href']
        first_a_href_list = first_a_href.split('/')
        first_a_href_len = len(first_a_href_list)
        first_id = first_a_href_list[first_a_href_len - 1]

        f_d_list = {'id': first_id, 'book_version_id': pare_list[5], 'book_version_name':pare_list[1],
                    'book_type_id': pare_list[3] ,'book_type_name': pare_list[2], 'point_name': each_first_point,
                    'subject': id_format[subj], 'father_id': 0}
        # print str(f_d_list['id']) + '  ' + f_d_list['book_version_id'] + '  ' + f_d_list['book_version_name'] + f_d_list['book_type_id'] + '  ' + f_d_list['book_type_name'] + '  ' + f_d_list['point_name'] + '  ' + str(f_d_list['father_id'])
        insert_table(f_d_list)

        second_point_ul = all_point_list[i].find_all('ul', recursive=False) # 二级知识点ul
        # 有的没有二级知识点
        # print second_point_ul
        second_point_ul_len = len(second_point_ul)
        if second_point_ul_len == 0:
            continue
        second_point_li = second_point_ul[0].find_all('li', recursive=False)  # 二级知识点li的list
        second_point_len = len(second_point_li)
        if second_point_len != 0:
            for spl in range(second_point_len):
                second_a = second_point_li[spl].find('label').find('a')
                second_point_name = second_a.text  # 二级知识点名称
                second_a_href = second_a['href']
                second_a_href_list = second_a_href.split('/')
                second_a_href_len = len(second_a_href_list)
                second_a_id = second_a_href_list[second_a_href_len - 1]

                s_d_list = {'id': second_a_id, 'book_version_id': pare_list[5], 'book_version_name':pare_list[1],
                            'book_type_id': pare_list[3] ,'book_type_name': pare_list[2], 'point_name': second_point_name,
                            'subject': id_format[subj], 'father_id':first_id}

                # print s_d_list['id'] + '  ' + s_d_list['book_version_id'] + '  ' + s_d_list['book_version_name'] + s_d_list['book_type_id'] + '  ' + s_d_list['book_type_name'] + '  ' + s_d_list['point_name'] + '  ' + s_d_list['father_id']
                insert_table(s_d_list)

                third_point_ul = second_point_li[spl].find_all('ul')  # 第三级知识点ul
                third_point_ul_len = len(third_point_ul)
                if third_point_ul_len == 0:  # 可能有三级也可能没有三级
                    continue
                # ul不为0，说明有三级知识点，继续寻找它的li
                # print third_point_ul
                third_point_li = third_point_ul[0].find_all('li', recursive=False)
                third_point_len = len(third_point_li)
                for tpl in range(third_point_len):
                    third_point_a = third_point_li[tpl].find('label').find('a')
                    third_point_name = third_point_a.text  # 三级知识点名称
                    third_point_href = third_point_a['href']
                    third_point_href_list = third_point_href.split('/')
                    third_point_href_len = len(third_point_href_list)
                    third_point_id = third_point_href_list[third_point_href_len-1]

                    t_d_list = {'id': third_point_id, 'book_version_id': pare_list[5], 'book_version_name':pare_list[1],
                            'book_type_id': pare_list[3] ,'book_type_name': pare_list[2], 'point_name': third_point_name,
                            'subject': id_format[subj], 'father_id': second_a_id}
                    # print t_d_list['id'] + '  ' + t_d_list['book_version_id'] + '  ' + t_d_list['book_version_name'] + t_d_list['book_type_id'] + '  ' + t_d_list['book_type_name'] + '  ' + t_d_list['point_name'] + '  ' + t_d_list['father_id']

                    insert_table(t_d_list)


@db_session
def insert_table(para_list):
    BookPoint(id=para_list['id'], book_version_id=para_list['book_version_id'], book_version_name=para_list['book_version_name'],
         book_type_id=para_list['book_type_id'],book_type_name=para_list['book_type_name'], point_name=para_list['point_name'],
         subject_name=para_list['subject'], father_id=para_list['father_id'])
    commit()


if __name__ == '__main__':
    get_tb_point()
