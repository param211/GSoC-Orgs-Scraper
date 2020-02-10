#! python3
# create speadsheet of gsoc organisations
from fake_useragent import UserAgent
import requests, bs4, openpyxl

'''ua = UserAgent()
header = {
    "User-Agent": ua.random
}'''


# Create list from html source code

url = 'https://summerofcode.withgoogle.com/archive/2018/organizations/'
res = requests.get(url)
res.raise_for_status()

language = 'python'
soup = bs4.BeautifulSoup(res.text, 'html.parser')
orgElem = soup.select('h4[class="organization-card__name font-black-54"]')


orgLink = soup.find_all("a", class_="organization-card__link")
languageCheck = ['no'] * len(orgElem)
orgURL = ['none'] * len(orgElem)
item = 0


for link in orgLink:

    presentLink = link.get('href')

    url2 = 'https://summerofcode.withgoogle.com' + presentLink
    print(item)
    print(url2)
    orgURL[item] = url2
    res2 = requests.get(url2)
    res2.raise_for_status()

    soup2 = bs4.BeautifulSoup(res2.text, 'html.parser')
    tech = soup2.find_all("li", class_="organization__tag organization__tag--technology")

    for name in tech:
        if language in name.getText():
            languageCheck[item] = 'yes'

    item = item + 1


# Write list to excel spreadsheet
wb = openpyxl.Workbook()
sheet = wb['Sheet']

for i in range(0, len(orgElem)):
    sheet.cell(row=i+1,column=1).value = orgElem[i].getText()
    sheet.cell(row=i+1,column=2).value = languageCheck[i]
    sheet.cell(row=i + 1, column=3).value = orgURL[i]

wb.save('gsocOrgsList.xlsx')
