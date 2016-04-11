#! python3
# downloadXkcd.py - Downloads every single XKCD comic.

import requests, os, bs4 ,sys, re

# Coding type for Chinese display: gb18030

keyword = ''.join(sys.argv[1:])
print("Keyword: " + keyword)

url = 'http://t66y.com'
os.makedirs('caoliu', exist_ok=True)

def SendUrl(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'gb18030'
    return response

def MakeSoup(text):
    return bs4.BeautifulSoup(text, 'html.parser')

print('Entering page %s...' % url)
res = SendUrl(url)
main_page = MakeSoup(res.text)
age_yes = main_page.select('a[href="index.php"]')
print("18 Yes Text:" + age_yes[0].text)
#for elem in age_yes:
#    print(elem.getText())
if age_yes ==[]:
    print('Could not fine 18 yes link')
else:
    age_yes_url = url + '/' + age_yes[0].get('href')
    print("18 yes link: " + age_yes_url)

forum_page = SendUrl(age_yes_url)
soup = MakeSoup(forum_page.text)

print('Searching for the link of 技術討論區...') # (jstlq)
main_part = soup.select('div[id="main"]')
soup = MakeSoup(str(main_part))
jstlq = soup.findAll(text=re.compile('技術討論區'))[0].parent.get('href')
jstlq_url = url + '/' +  jstlq
print('技術討論區 URL: ' + jstlq_url)

print('Entering 技術討論區...')
page = SendUrl(jstlq_url)
print('Succeed! Exciting!')

print('Searching for the posts with the keyword: ' + keyword + '...')
soup = MakeSoup(page.text)
posts = soup.findAll(text=re.compile(keyword))
if len(posts) == 0:
    print('No posts contain ' + keyword)
else:
    print('Found ' + str(len(posts)) + ' posts. Exciting!')
    i = 1
    for post in posts:
        print('<' + str(i) + '> ' + post.string)
        print('Link: ' + str(post.parent.get('href')))
        i=i+1
    
    print('Enter first found link...')
    first_url = url + '/' + posts[0].parent.get('href')
    res = SendUrl(first_url)
    soup = MakeSoup(res.text)
    page_main_region = soup.find('div',{'class':'tpc_content do_not_catch'})
    print('Post content:\n' + page_main_region.text)
    #gif = soup.findAll('img',{'src':re.compile(r'\w+.gif')})
    #gif = soup.select(img[src=re.compile(r'\w+.gif')])
    soup = MakeSoup(str(page_main_region))
    img_tags = soup.findAll('img')
    print('# of GIF: ' + str(len(img_tags)))
    print('\n'.join(set(tag['src'] for tag in img_tags)))

#print('技术讨论区text：')
#for string in soup.stripped_strings:
#    print(string)

#tz = soup.select('tr td[style] h3 a')
#print(' 技術討論區 帖子数量：' + str(len(tz)))

#for t in tz:
#    print(t.text)
print('Done.')
