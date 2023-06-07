from classes.general_spider import GeneralSpider
from envar import *
import time

if __name__ == "__main__":
    start = time.time()

    brand_to_scrape = input("For what keywords do you want to search on website?: ")
    sig_spider = GeneralSpider(brand_to_scrape)
    time.sleep(SMALL_DELAY)
    sig_spider.write_to_search_input()
    time.sleep(SMALL_DELAY)
    data_dict = sig_spider.get_product_dataset()
    time.sleep(SMALL_DELAY)
    sig_spider.save_file_to_json(data_dict)
    sig_spider.save_file_to_csv(data_dict)
    time.sleep(SMALL_DELAY)
    sig_spider.save_images(data_dict)
    #
    end = time.time()
    print(sig_spider.success_msg + f"SigSpider execution time: {round(end - start, 2)} seconds.")

    sig_spider.driver.close()