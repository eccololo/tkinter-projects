from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from colorama import Fore, Back, Style
import pandas as pd
import requests
import os
import time
import shutil
import json

SMALL_DELAY = 1
MEDIUM_DELAY = 3
BIG_DELAY = 6
TARGET_WEBSITE = ""


class GeneralSpider:

    def __init__(self, keywords, driver="chromedriver_v112.exe"):

        self.success_msg = "[" + Fore.GREEN + "Success" + Style.RESET_ALL + "] "
        self.error_msg = "[" + Fore.RED + "Error" + Style.RESET_ALL + "] "
        self.error_details_msg = "[" + Fore.RED + "Details" + Style.RESET_ALL + "] "
        self.keywords = keywords.replace(" ", "-")
        self.target_website = TARGET_WEBSITE
        self.output_data_json_filename = f"{self.keywords}-dataset-1.json".lower()
        self.output_data_csv_filename = f"{self.keywords}-dataset-1.csv".lower()
        self.output_data_dir = "output/data"
        self.output_images_dir = "output/images"
        self.opts = None
        self.ua = None
        self.driver_path = shutil.which(driver)
        self.set_driver_options()
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=self.opts)
        self.driver.implicitly_wait(10)
        self.driver.get(self.target_website)
        self.page_source = self.get_page_source()
        self.soup = None
        self.set_soup_obj()
        self.dom = self.get_dom_obj()

        self.invalid_chars = "ĄąĆćĘęŁłŃńÓóŚśŹźŻż"
        self.invalid_chars_unicode_list = [u"\xa0"]
        self.valid_chars = "AaCcEeLlNnOoSsZzZz"

    def set_driver_options(self):
        self.opts = Options()
        self.ua = UserAgent()
        self.opts.add_argument(f"user-agent={self.ua.chrome}")
        self.opts.add_argument("--headless")

    def get_page_source(self):
        return self.driver.page_source

    def write_to_search_input(self):
        """This method writes to search input specific keyword on Sig.pl website."""
        # 1. [SELECTOR] - To Adjust:
        search_input = self.driver.find_element(By.CLASS_NAME, "<selector>")
        search_input.send_keys(self.keywords)
        time.sleep(SMALL_DELAY)
        search_input.submit()
        time.sleep(SMALL_DELAY)

    def get_prod_page_links(self):
        """This method return us a list of links to product pages."""
        self.set_soup_obj()
        self.dom = self.get_dom_obj()

        # 2. [SELECTOR] - To Adjust:
        prod_page_links = self.dom.xpath("<selector>")

        return prod_page_links

    def set_soup_obj(self, source_data=""):
        """This method returns us a BeautifulSoup object."""
        if source_data:
            self.soup = BeautifulSoup(source_data, "lxml")
        else:
            self.soup = BeautifulSoup(self.get_page_source(), "lxml")

    def get_dom_obj(self):
        """This method returns us a dom object of etree module."""
        return etree.HTML(str(self.soup))

    def get_product_dataset(self):
        product_dataset = {}
        products_links = self.get_prod_page_links()
        headers = self.get_fake_user_agent_dict()
        for idx, link in enumerate(products_links):
            product_data_dict = {}

            # [TESTING] - To Adjust:
            if idx >= 2:
                break

            idx += 1
            time.sleep(MEDIUM_DELAY)
            print("[" + Fore.BLUE + f"Product_{idx}" + Style.RESET_ALL + "]" + ": Scraping data ...")
            response = requests.get(link, timeout=5, headers=headers)
            if response.status_code == 200:
                self.set_soup_obj(str(response.text))
                self.dom = self.get_dom_obj()

                # 3. [SELECTOR] - To Adjust:
                # XPath Selectors - Product Page

                element_1 = "<selector>"
                element_2 = "<selector>"
                user_agent = self.driver.execute_script("return navigator.userAgent")

                product_data_dict["key_1"] = "".join(self.dom.xpath(element_1)).replace("\\n",
                                                                                                       "").strip() if len(
                    "".join(self.dom.xpath(element_1))) != 0 else "Not Found"

                image_element = self.soup.find_all("img", {"<attribute>": "<selector>"})
                product_data_dict["img_src"] = image_element[0]["src"]

                product_data_dict["URL"] = response.url
                product_data_dict["User-Agent"] = user_agent

                product_data_dict["key_4"] = "".join(self.dom.xpath(element_2)).replace("\\n", "").replace(
                    "<to_replace>", "").strip() if len(
                    "".join(self.dom.xpath(element_2))) != 0 else "Not Found"

                print("[" + Fore.BLUE + f"Product_{idx}" + Style.RESET_ALL + "]" + ": Saving data ...")

                # Cleaning data in output dict:
                product_data_dict = self.clean_output_data_from_unicode_chars(product_data_dict)

                product_dataset[f"dataitem_{idx}"] = product_data_dict

        return product_dataset

    def get_fake_user_agent_dict(self):
        return {"User-Agent": self.ua.chrome}

    def save_file_to_json(self, x_dataset):
        """This method saves output data to a either JSON or CSV data file."""

        dir_path = os.path.join(os.getcwd(), self.output_data_dir)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        file_path = os.path.join(os.getcwd(), self.output_data_dir, self.output_data_json_filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(x_dataset, f, indent=4, ensure_ascii=False)
            print(self.success_msg + "Data saved to JSON file ...")

    def save_file_to_csv(self, x_data):
        file_path = os.path.join(os.getcwd(), self.output_data_dir, self.output_data_csv_filename)
        dir_path = os.path.join(os.getcwd(), self.output_data_dir)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        df = pd.DataFrame.from_dict(x_data, orient="index")
        df.to_csv(file_path)
        print(self.success_msg + "Data saved to CSV file ...")

    def save_images(self, data):
        """This method saves images from a domain from previously extracted images src list."""

        for idx, d in enumerate(data.values()):
            idx += 1

            # 4. [DICT SELECTOR] - To Adjust
            image_url = d["image_src"]
            prod_title = d["prod_title"].split(" ")[0] if d["prod_title"] != "Not Found" else "unknown_t"
            prod_brand = d["prod_brand"].replace(" ", "") if d["prod_brand"] != "Not Found" else "unknown_b"

            image_name = prod_title + "_" + prod_brand + f"_{idx}.jpg"
            image_name = image_name.lower()

            image_name = self.clean_file_name(image_name)

            idx += 1
            time.sleep(BIG_DELAY)
            response = requests.get(image_url, stream=True)

            if response.status_code == 200:
                image_path = os.path.join(os.getcwd(), self.output_images_dir, image_name)

                dir_path = os.path.join(os.getcwd(), self.output_images_dir)
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)

                try:
                    with open(image_path, "wb") as f:
                        shutil.copyfileobj(response.raw, f)
                except FileNotFoundError as e:
                    print(self.error_msg + f"Something went wrong during saving the file: {image_name}.")
                    print(self.error_details_msg + f"{e}")
                else:
                    print(self.success_msg + f"Image {image_name} saved succesfully ...")

        print(self.success_msg + "Images saved succesfully ...")

    def clean_file_name(self, file_name):
        """These methods clean file name from invalid chars and return cleaned file name."""

        for x_chars in zip(self.invalid_chars, self.valid_chars):
            file_name = file_name.replace(x_chars[0], x_chars[1])

        return file_name

    def clean_output_data_from_unicode_chars(self, output_data):
        cleaned_output_data_dict = {}
        for unicode_char in self.invalid_chars_unicode_list:
            for key, value in output_data.items():
                if unicode_char in value:
                    if unicode_char == u"\xa0":
                        value = value.replace(unicode_char, " ")
                cleaned_output_data_dict[key] = value

        return cleaned_output_data_dict


