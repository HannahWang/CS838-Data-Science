from bs4 import BeautifulSoup
import re
import csv

RPP = 30
NEED = 3100
N_PG = int(NEED/RPP) + 1

def read_soup(url, decode_type=None):
    import requests
    r = requests.get(url)
    encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding=encoding)
    return soup


class Restaurant:
    def __init__(self, idx, name, single_page_url):
        self.id = idx
        self.name = name
        self.url = single_page_url
        self.rate = None
        self.reviews = None
        self.money = None
        self.type = list()
        self.address_street = None
        self.address_locality = None
        self.phone = None
        self.sun_hours = None
        self.mon_hours = None
        self.tues_hours = None
        self.wed_hours = None
        self.thur_hours = None
        self.fri_hours = None
        self.sat_hours = None
        self.crawl_from_url()

    def set_hours(self, day_text, hours):
        if day_text == "Sunday":
            self.sun_hours = hours
        elif day_text == "Monday":
            self.mon_hours = hours
        elif day_text == "Tuesday":
            self.tues_hours = hours
        elif day_text == "Wednesday":
            self.wed_hours = hours
        elif day_text == "Thursday":
            self.thur_hours = hours
        elif day_text == "Friday":
            self.fri_hours = hours
        elif day_text == "Saturday":
            self.sat_hours = hours

    def crawl_from_url(self):
        try:
            soup = read_soup(self.url)
            header_rating = soup.find(class_="header_rating")
            self.rate = header_rating.find("span", {"property": "ratingValue"})["content"]
            self.reviews = header_rating.find("span", {"property": "count"}).text.replace(",", "")
            header_money = soup.find(class_="header_tags rating_and_popularity")
            self.money = header_money.text if header_money else None
            header_types = soup.find(class_="header_links rating_and_popularity")
            self.type = [t.text for t in header_types.find_all("a")] if header_types else list()
            header_street = soup.find(class_="street-address")
            self.address_street = header_street.text if header_street else None
            header_locality = soup.find(class_="locality")
            self.address_locality = header_locality.text if header_locality else None
            header_phone = soup.find(class_="ui_icon phone").next_sibling
            self.phone = header_phone.text if header_phone else None
            hours = soup.find(class_="hours content")
            if hours:
                week = hours.find(class_="detail")
                while week:
                    self.set_hours(week.find(class_="day").text, week.find(class_="hoursRange").text)
                    week = week.next_sibling.next_sibling
        except Exception as e:
            print(e)
            print("{} {} \n{}".format(self.id, self.name, self.url))

    def writerow_to_csv(self, csvwriter):
        info = [self.id, self.name, self.rate, self.reviews, self.money]
        for i in range(3):
            try:
                info.append(self.type[i])
            except IndexError:
                info.append(None)
        info.extend([self.address_street, self.address_locality, self.phone])
        info.extend([self.sun_hours, self.mon_hours, self.tues_hours, self.wed_hours, self.thur_hours, self.fri_hours, self.sat_hours])
        csvwriter.writerow(info)


# crawl website information
idx = 1
restaurants = list()
print("Start crawling")
for page in range(N_PG):
    API_url = 'https://www.tripadvisor.com/RestaurantSearch?Action=PAGE&geo=32655&ajax=1&itags=10591&sortOrder=relevance&o=a{}&availSearchEnabled=false'\
            .format(page*30)
    soup = read_soup(API_url)
    reslist_regex = re.compile(".*listing.*")
    reslist = soup.find_all("div", class_=reslist_regex)
    for res in reslist:
        title = res.find(class_="property_title")
        name = title.text.strip()
        url = "https://www.tripadvisor.com" + title['href']
        r_object = Restaurant(idx, name, url)
        restaurants.append(r_object)
        idx += 1

# convert to csv
print("Start convert to csv")

with open('tripadvisor_la.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["id", "name", "rate", "n_reviews", "money", "type_1", "type_2", "type_3", "address_street", "address_locality", "phone", \
                        "sun_hours", "mon_hours", "tue_hours", "wed_hours", "thur_hours", "fri_hours", "sat_hours"])
    for robj in restaurants:
        robj.writerow_to_csv(csvwriter)
