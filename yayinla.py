#!/bin/python
import sys
import markdown 
import datetime
import os
from bs4 import BeautifulSoup




dosyaadi =  sys.argv[1]
dosyaadihtml = dosyaadi.replace(".md",".html")

aylar = {
    1: 'Oca', 2: 'Şub', 3: 'Mar', 4: 'Nis', 5: 'May', 6: 'Haz',
    7: 'Tem', 8: 'Ağu', 9: 'Eyl', 10: 'Eki', 11: 'Kas', 12: 'Ara'
    }
# Mevcut tarihi al
simdiki_tarih = datetime.datetime.now()
# Gün, ay ve yıl bilgisini al
gun = simdiki_tarih.day
ay = simdiki_tarih.month
yil = simdiki_tarih.year
# Türkçe ve kısaltılmış tarih formatını oluştur
tarih = f"{gun} {aylar[ay]} {yil}"
yil = str(yil)
ay = str(ay)
klasoryolu = "./site/yazilarim/"+yil+"/"+ay

with open(dosyaadi, 'r', encoding='utf-8') as md_file:
    md_icerik = md_file.read()



html_icerik = markdown.markdown(md_icerik)


html_sablon = """
<!DOCTYPE html>
<html>
	<meta charset="UTF-8">
	<link rel="stylesheet" href="../../../css/style.css">
	<title>{baslik}</title>
    {markdown_icerik}
</html>
"""


soup = BeautifulSoup(html_icerik, 'html.parser')
h1_tags = soup.find_all('h1')
if len(h1_tags) != 1:
    raise ValueError("Markdown dosyasında Bir Başlık Olmalı. İşlem iptal edildi.")
baslik = h1_tags[0].text

if not os.path.exists(klasoryolu):
    os.makedirs(klasoryolu)

with open('./site/index.html', 'r', encoding='utf-8') as index_icerik:
    index_soup = BeautifulSoup(index_icerik, 'html.parser')
    ul_tag = index_soup.find('ul')
    new_li_tag = index_soup.new_tag('li')
    br_tag = index_soup.new_tag('br')
    span_tag = index_soup.new_tag('span', attrs={"class": "yazi-tarihi"})
    span_tag.string = tarih 
    h3_tag = index_soup.new_tag('h3', attrs={"style": 'margin-top:0px'})
    a_tag = index_soup.new_tag('a', attrs={"class": "yazi-link", "href": './yazilarim/'+yil+'/'+ay+'/'+dosyaadihtml})
    a_tag.string = baslik
    new_li_tag.append(br_tag)
    new_li_tag.append(span_tag)
    new_li_tag.append(h3_tag)
    h3_tag.append(a_tag)
    ul_tag.insert(0, new_li_tag)
    guncel_index_icerik = str(index_soup)



final_html = html_sablon.format(markdown_icerik=html_icerik, baslik=baslik)
final_html = final_html.replace("</h1>", '</h1><span class="yazi-tarihi">' + tarih +'</span>')



if os.path.exists(klasoryolu +'/'+ dosyaadihtml):
    raise Exception('Zaten Yayinlanmis !!!!')

with open(klasoryolu+'/'+dosyaadihtml, 'w', encoding='utf-8') as yeniyazi:
    yeniyazi.write(final_html)

os.rename(dosyaadi, 'eskiyazilar/' + dosyaadi)

with open('./site/index.html', 'w', encoding='utf-8') as guncel_anasayfa:
    guncel_anasayfa.write(guncel_index_icerik)



