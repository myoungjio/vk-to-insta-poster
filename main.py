# -*- coding:utf-8 -*-
import urllib2
import urllib
from pyquery import PyQuery
from BeautifulSoup import BeautifulSoup
import re
import os
from os import listdir
from os.path import isfile, join
from InstagramAPI import InstagramAPI
from resizeimage import resizeimage
import PIL

PhotoPath = "/home/user/image"  # Change Directory to Folder with Pics that you want to upload
os.chdir(PhotoPath)

# TAG = re.compile(r'<[^/>]+/>')
TAG_RE = re.compile(r'<[^>]+>')
TAG = re.compile(r'(<br>)|(<\/br>)|(<br \/>)')
space = re.compile(r'\s+(?=<)')
# remove spaces before tags
def rem_space(text):
    return space.sub('',text)
#Replase <br> with \n
def br_to_r(text):
    return TAG.sub("\r\n" ,text)

# Remove tag from post
def remove_tags(text):
    return TAG_RE.sub('', text)


# GET POST FORM VK
resp = urllib2.urlopen('https://vk.com/yourgroup')
html = resp.read()
parsed_html = BeautifulSoup(html)
starttx = '<span>'
endtx = '</div>'
start = 'background-image: url('
end = 'jpg'
# print(parsed_html)
text = parsed_html.body.findAll('div', attrs={'class': 'pi_text'})
text = str(text)
# print('parsed text',text)  #for debug

text = text[text.find(starttx) + len(starttx):text.find(endtx)]
text = unicode(text, "utf-8")
text = text.replace(u"Показать полностью…", '')
text = rem_space(text)
# print('After remove space', text) #for debug
text=br_to_r(text)
# print('After BR TO TExt',text) #for debug
# parse and trim img url
img = parsed_html.body.findAll('div', attrs={'class': 'thumb_map_img thumb_map_img_as_div'})
img = str(img)
img = img[img.find(start) + len(start):img.find(end) + len(end)]
print('img path', img)
# get img localy
f = open("1.jpg", 'wb')
f.write(urllib.urlopen(img).read())
f.close()
# IMG RESIZE 1
# with open('1.jpg', 'r+b') as f:
#     with Image.open(f) as image:
#         cover = resizeimage.resize_cover(image, [1040, 1040],validate=False)
#         cover.save('1.jpg', image.format)
# f.close()
# IMG RESIZE 2
# basewidth = 1090
# image = Image.open('1.jpg')
# wpercent = (basewidth / float(image.size[0]))
# hsize = int((float(image.size[1]) * float(wpercent)))
# image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
# image.save('1.jpg')
# print('Remove Tag text',remove_tags(text)) #for debug
text = remove_tags(text)
# START POSTING

#

IGUSER = "USERNAME"  # Change to your Instagram USERNAME
PASSWD = "Password"  # Change to your Instagram Password
# Change to your Photo Hashtag
IGCaption = text + "\n#yourhashtags"
# os.chdir(PhotoPath)
ListFiles = sorted([f for f in listdir(PhotoPath) if isfile(join(PhotoPath, f))])
print('File list',ListFiles)
photo = '1.jpg'
print("Total Photo in this folder:" + str(len(ListFiles)))
#
## Start Login and Uploading Photo
igapi = InstagramAPI(IGUSER, PASSWD)
igapi.login()  # login
igapi.uploadPhoto(photo, caption=IGCaption, upload_id=None)
# ## END posting
#

#for mass posting
# for i, _ in enumerate(ListFiles):
#     photo = ListFiles[i]
#     print("Progress :" + str([i + 1]) + " of " + str(len(ListFiles)))
#     print("Now Uploading this photo to instagram: " + photo)
#     igapi.uploadPhoto(photo, caption=IGCaption, upload_id=None)
#     os.remove(photo)
#     # sleep for random between 60 - 120s
#     n = randint(700,900)
#     print("Sleep upload for seconds: " + str(n))
# time.sleep(n)
os.remove(photo)
