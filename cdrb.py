import urllib.request
import easygui as g
import time as t
import os
import sys

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()

    return html


def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []
    
    a = html.find('a class="pdf" href=')
    
    while a != -1:
        b = html.find('.pdf', a, a+255)
        if b != -1:
            src = html[a+20:b+4]
            print(src)
            img_addrs.append(src)
            b = a + 20
            a = html.find('a class="pdf" href=', b)

    return img_addrs

def save_imgs(folder, img_addrs, page):
    
    filename = 'The page ' + str(page) + '.pdf'
    for each in img_addrs:
        with open(filename, 'wb') as f:
            img = url_open(each)
            f.write(img)
            
def find_date():

    date_list = []
    
    istoday = g.boolbox(msg='是否获取今日的成都日报?', title='By DCZ', choices=('Yes','No'))
    if istoday:
        date_list.append(str(t.localtime().tm_year))
        #date_list.append(str(t.localtime().tm_mon))
        if t.localtime().tm_mon < 10:
            single_mon = '0' + str(t.localtime().tm_mon)
            date_list.append(single_mon)
        else:
            date_list.append(str(t.localtime().tm_mom))
        if t.localtime().tm_mday < 10:
            single_day = '0' + str(t.localtime().tm_mday)
            date_list.append(single_day)
        else:
            date_list.append(str(t.localtime().tm_mday))
    else:
        try: 
        
            date = g.enterbox(msg='请输入最近两月(月/日)单数请补零！！！',title='成都日报索取')

            date_list.append(str(t.localtime().tm_year))
            date_list.append(date.split('/')[0])
            date_list.append(date.split('/')[1])

            if int(date_list[1]) > 12 or \
               int(date_list[2]) > 31:
                g.msgbox('年月日是多少心里没点数？退了T^T')
                sys.exit()
        except IndexError:
            g.msgbox(msg='请按要求输入!!!')
            find_date()
        except AttributeError:
            sys.exit()

    return date_list
    
def download__pdf(folder = 'cdrb'):

    news_date = find_date()

    folder = folder + news_date[0] + news_date[1] + news_date[2]
    
    os.mkdir(folder)
    os.chdir(folder)

    url_temp = 'http://www.cdrb.com.cn/epaper/cdrbpc/' + news_date[0] + news_date[1] + '/' + news_date[2] + '/' + 'l'
    temp = 1
    try:
        for i in range(16):
            if temp < 10:
                url = url_temp + '0' + str(temp) + '.html'
            else:
                url = url_temp + str(temp) + '.html'
            img_addrs = find_imgs(url)
            save_imgs(folder, img_addrs, temp)
            temp += 1
    except urllib.error.HTTPError:
        pass

if __name__ == '__main__':
    download__pdf()
