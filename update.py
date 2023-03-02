import threading
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request
import os
import shutil
import random
import string

# Function to create or recreate folder "Images" and file "DB.txt"
def refresh_os():
    with open('DB.txt', 'wb'):
        pass
    images_path = 'Images'
    if not os.path.exists(images_path):
        os.mkdir(images_path)
    else:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), images_path)
        shutil.rmtree(path)
        os.mkdir(images_path)

# The function of adding records from the pharmacy "Аптека от склада" to the database
def apteka_ot_sklada():
    length_range = 1450
    first_number = 0
    second_number = 2
    for i in range(length_range):
        try:
            temporary_storage_img = []
            temporary_storage_name = []
            temporary_storage_price = []
            # Setting a link
            url = "https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady?start="
            if first_number == 0:
                url = url + str(first_number) + "&sort=name"
                first_number = first_number + 1
            else:
                if second_number > 8:
                    second_number = 0
                    first_number = first_number + 1
                url = url + str(first_number) + str(second_number) + "&sort=name"
                first_number = first_number + 1
                second_number = second_number + 2
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            query_result = soup.findAll('img', class_='goods-photo goods-card__image')
            # Downloading a picture and adding img title to list
            for data in query_result:
                value = data.get('src')
                value = value[len(value)::-1]
                value = value.split('/')[0]
                value = value[len(value)::-1]
                pass_url = "https://apteka-ot-sklada.ru/images/goods/" + value
                request_site = Request(pass_url, headers={"User-Agent": "Mozilla/5.0"})
                download_img = urllib.request.urlopen(request_site).read()
                letters = string.ascii_lowercase
                # Adding a random value to the img name
                rand_string = ''.join(random.choice(letters) for j in range(8))
                value = rand_string + value
                path_images = open("Images/{}".format(value), 'wb')
                path_images.write(download_img)
                path_images.close()
                temporary_storage_img.append(value)
            query_result = soup.findAll('a', class_='goods-card__link')
            # Adding name to list
            for data in query_result:
                value = data.getText()
                temporary_storage_name.append(value)
            query_result = soup.findAll('span', class_='goods-card__cost text text_size_title text_weight_bold')
            # Adding price to list
            for data in query_result:
                value = data.getText()
                # Adding only numbers
                string_line = ""
                for j in value:
                    if '0' <= j <= '9' or j == ".":
                        string_line = string_line + j
                value = "от " + string_line + " руб."
                temporary_storage_price.append(value)
            # Connection all lists
            query_result = [list(a) for a in
                            zip(temporary_storage_img, temporary_storage_name, temporary_storage_price)]
            # Writing to a text file
            f = open('DB.txt', 'a')
            for j in range(len(query_result)):
                query_result[j].append("Аптека от склада")
                f.write(str(query_result[j]) + '\n')
            f.close()
        except:
            print("[INFO] Error Update Apteka_ot_Sklada")

# The function of adding records from the pharmacy "Фармакопейка" to the database
def farmakopeika():
    length_range = 570
    for i in range(1, length_range):
        try:
            temporary_storage_img = []
            temporary_storage_name = []
            temporary_storage_price = []
            url = "https://farmakopeika.ru/catalog/2440?availability=is_available&without_rx_only=0&has_discount_only" \
                  "=0&has_gifts_only=0&limit=12&page=" + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            query_result = soup.findAll('img', class_='product__photo')
            for data in query_result:
                value = data.get('src')
                value = value[len(value)::-1]
                value = value.split('/')[0]
                value = value[len(value)::-1]
                try:
                    pass_url = "https://farmakopeika.ru/storage/products/" + value
                    request_site = Request(pass_url, headers={"User-Agent": "Mozilla/5.0"})
                    download_img = urllib.request.urlopen(request_site).read()
                except:
                    pass_url = "https://farmakopeika.ru/images/" + value
                    request_site = Request(pass_url, headers={"User-Agent": "Mozilla/5.0"})
                    download_img = urllib.request.urlopen(request_site).read()
                letters = string.ascii_lowercase
                rand_string = ''.join(random.choice(letters) for j in range(8))
                value = rand_string + value
                path_images = open("Images/{}".format(value), 'wb')
                path_images.write(download_img)
                path_images.close()
                temporary_storage_img.append(value)
            query_result = soup.findAll('div', class_='product__title')
            for data in query_result:
                value = data.getText()
                value = value.split('\n')[1]
                temporary_storage_name.append(value)
            query_result = soup.findAll('span', class_='product__price-text')
            for data in query_result:
                value = data.getText()
                string_line = ""
                for j in value:
                    if '0' <= j <= '9' or j == ".":
                        string_line = string_line + j
                value = "от " + string_line + " руб."
                temporary_storage_price.append(value)
            query_result = [list(a) for a in
                            zip(temporary_storage_img, temporary_storage_name, temporary_storage_price)]
            f = open('DB.txt', 'a')
            for j in range(len(query_result)):
                query_result[j].append("Фармакопейка")
                f.write(str(query_result[j]) + '\n')
            f.close()
        except:
            print("[INFO] Error Update Farmakopeika")

# The function of adding records from the pharmacy "Семейная аптека" to the database
def family_apteka():
    try:
        temporary_storage_img = []
        temporary_storage_name = []
        temporary_storage_price = []
        url = "https://xn----7sbatzcnpe0ae.xn--p1ai/catalog/lekarstvennye-sredstva"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        query_result = soup.findAll('div', class_='h2')
        for i in range(len(query_result)):
            value = "photo.png"
            temporary_storage_img.append(value)
        for data in query_result:
            value = data.getText()
            temporary_storage_name.append(value)
        query_result = soup.findAll('div', class_='price-new')
        for data in query_result:
            value = data.getText()
            string_line = ""
            for j in value:
                if '0' <= j <= '9' or j == ".":
                    string_line = string_line + j
            value = "от " + string_line + " руб."
            temporary_storage_price.append(value)
        temporary_storage_price.insert(0, 1)
        query_result = [list(a) for a in zip(temporary_storage_img, temporary_storage_name, temporary_storage_price)]
        f = open('DB.txt', 'a')
        for i in range(len(query_result)):
            query_result[i].append("Семейная аптека")
            f.write(str(query_result[i]) + '\n')
        f.close()
    except:
        print("[INFO] Error Update Family_Apteka")

# Database update
def update_db():
    print("[INFO] Start update!")
    refresh_os()
    # Separate threads of execution, to speed up the program
    x = threading.Thread(target=apteka_ot_sklada)
    y = threading.Thread(target=farmakopeika)
    z = threading.Thread(target=family_apteka)
    x.start()
    y.start()
    z.start()
    x.join()
    y.join()
    z.join()
    print("[INFO] DB was updated!")

if __name__ == '__main__':
    update_db()
