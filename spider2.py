#encoding :utf-8
from urllib import request
from bs4 import BeautifulSoup as bs
import pandas as pd

#定义获取网页电影名称及id
def getNowplayingMovie_list():
    url = request.urlopen('https://movie.douban.com/cinema/nowplaying/suzhou/')
    html_data = url.read().decode('utf-8')
    soup = bs(html_data,'html.parser')
    nowplaying_movie = soup.find_all('div', id="nowplaying")
    #print(nowplaying_movie)
    nowplaying_movie_list = nowplaying_movie[0].find_all('li',class_='list-item')
    #print(nowplaying_movie_list)[0]
    nowplaying_list = []     #存放电影id和名称
    for item in nowplaying_movie_list:
        nowplaying_dict = {}    #存放电影id
        nowplaying_dict['id'] = item['data-subject']
        for tag_img_item in item.find_all('img'):   #找到img标签里的alt即电影名称
            nowplaying_dict['name'] = tag_img_item['alt']
            nowplaying_list.append(nowplaying_dict)
    return nowplaying_list  #返回带有id和名称的列表


def getCommentsById(movieId,pageNum):
    eachCommentList = []
    if pageNum>0:
        start = (pageNum-1) * 20
    else:
        return False
    requrl = 'https://movie.douban.com/subject/'+movieId+'/comments'+'?'+'start='+str(start)+'&limit=20'
    #print(requrl)
    url = request.urlopen(requrl)
    html_data = url.read().decode('utf-8')
    soup = bs(html_data,'html.parser')
    comment_div_lists = soup.find_all('div',class_='comment')

    for item in comment_div_lists:
        if item.find_all('p')[0].string is not None:
            eachCommentList.append(item.find_all('p')[0].string)
    return eachCommentList



def main():
    commentList = []
    NowplayingMovie_list = getNowplayingMovie_list()

    for i in range(12):
            num = i+1

            commentList_temp = getCommentsById(NowplayingMovie_list[0]['id'],num)
            commentList.append(commentList_temp)

    #数据清洗，将数据转换为字符串
    comments = ''
    for k in range(len(commentList)):
        comments = comments + (str(commentList[k])).strip()
    print(comments)

main()

