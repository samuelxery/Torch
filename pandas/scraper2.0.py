from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
driver = webdriver.Chrome()
scraped_data = []
# main loop :p
for i in range(1, 51):
    site_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    driver.get(site_url)
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    book_urls = []
    for book in books:
        element = book.find_element(By.CSS_SELECTOR, "h3 a")
        book_urls.append(element.get_attribute("href"))
        
    for url in book_urls:
        driver.get(url)
        details = driver.find_elements(By.CLASS_NAME, "product_page")
        main_details = driver.find_element(By.CSS_SELECTOR, "div.col-sm-6.product_main")
        title = main_details.find_element(By.TAG_NAME, "h1").text
        price = main_details.find_element(By.CLASS_NAME, "price_color").text
        for detail in details:
            try:
                description = driver.find_element(By.XPATH, "//*[@id='content_inner']/article/p").text
                upc = driver.find_element(By.XPATH, "//*[@id='content_inner']/article/table/tbody/tr[1]/td").text
                genre = driver.find_element(By.XPATH, "//*[@id='default']/div/div/ul/li[3]/a").text
            except:
                continue
        scraped_data.append({
            "title": title,
            "price": price,
            "description": description,
            "UPC": upc,
            "genre": genre
        })
df = pd.DataFrame(scraped_data)
df.to_json("bookss.jsonl", orient="records", lines=True)