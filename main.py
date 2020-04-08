from bs4 import BeautifulSoup

# urllib = package
# request = module
# urlopen = function
from urllib.request import urlopen as uReq

import re
import csv

# Open the file and use csv.DictWriter
# Write to the file header
csv_file = open('Katowice_flat_data.csv', mode='w', newline ='',  encoding='utf-8')
writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['District', 'Area', 'Rooms', 'Total price', 'Price per meter square'])

# find the number of subsites:
# before, we have to grab the first page:
uClient = uReq('https://gratka.pl/nieruchomosci/mieszkania/katowice/sprzedaz')
page_html = uClient.read()
uClient.close()
page_soup = BeautifulSoup(page_html, "html.parser")
subsites = int(page_soup.findAll("div", {"class": "pagination"})[0].text.split("\n")[-3])

# generate list of substites' urls
url_list = ['https://gratka.pl/nieruchomosci/mieszkania/katowice/sprzedaz']
for i in range(subsites):
    url_list.append('https://gratka.pl/nieruchomosci/mieszkania/katowice/sprzedaz?page=' + str(i+1))

for url in url_list:
    # opening up connection, grabbing the page
    uClient = uReq(url)
    # offloads the content to a variable
    page_html = uClient.read()
    # closes the connection
    uClient.close()

    # html parsing
    # ---
    # to parse = resolve (a sentence) into its component parts and describe their syntactic roles
    # = taking in HTML code and extracting relevant information like the title of the
    # page, paragraphs in the page, headings in the page, links, bold text etc
    page_soup = BeautifulSoup(page_html, "html.parser")

    # assign all html boxes to flat_containers (which is an array)
    # all divs that have the class [tag] "teaser__content" [name]
    flat_containers = page_soup.findAll("div", {"class":"teaser__content"})

    # loop over every container in given subsite
    for flat_container in flat_containers:
        # 1
        # Find district name
        # ---
        # save the district name in the list - length 0 if none given
        district_name=''
        district_list = flat_container.find("h3", {"class":"teaser__location"}).text.split()[1:-1]
        district_list_edited = district_list
        # if district name given, remove the comma in the last word if present
        if len(district_list)>0:
            if district_list[-1][-1]==',':
                district_list_edited[-1] = district_list[-1][0:-1]
            district_name=" ".join(district_list_edited)
        else:
            district_name = "N/A"

        # 2 & 3
        # Find flat area & number of rooms
        # ---
        # Find the part containing flat area & no. of rooms and save it into a list
        area_rooms_list = flat_container.findAll("ul", {"class": "teaser__params"})[0].text.split("\n")
        # Find on which positions is area an no. of rooms
        i = 0
        match_area_index = -1
        match_rooms_index = -1
        for area_rooms_list_elements in area_rooms_list:
            if re.search(r'Powierzchnia', area_rooms_list_elements):
                match_area_index = i
            if re.search(r'poko', area_rooms_list_elements):
                match_rooms_index = i
            i += 1
        # Get area
        if match_area_index != -1:
            flat_area = float(area_rooms_list[match_area_index].split()[-1])
        # Get number of rooms
        if match_rooms_index != -1:
            room_number = int(area_rooms_list[match_rooms_index].split()[-1])

        # 4 & 5
        # Find flat price and price per meter square
        # ---
        # Check whether there is price given
        # If price given, get the price and price per m2
        if flat_container.findAll("span", {"class": "teaser__priceAdditional"}):
            flat_price = float(re.sub(r'\s+', '', flat_container.findAll("p", {"class": "teaser__price"})[0].text.split("\n")[1])[0:-2])
            flat_price_per_m2 = float(re.sub(r'\s+', '', flat_container.findAll("span", {"class": "teaser__priceAdditional"})[0].text[0:-6]))
        else:
            flat_price = 'N/A'
            flat_price_per_m2 = 'N/A'

        # 1st row: writer.writerow(['District', 'Area', 'Rooms', 'Total price', 'Price per meter square'])
        writer.writerow([district_name, flat_area, room_number, flat_price, flat_price_per_m2])

        # print("district: "+ district_name )
        # print("area: " + str(flat_area))
        # print("rooms: " + str(room_number))
        # print("price_total: " + str(flat_price))
        # print("price_m2: " + str(flat_price_per_m2) + "\n")


csv_file.close()