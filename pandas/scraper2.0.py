from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
driver = webdriver.Chrome()
scraped_data = []
# main loop :p
for i in range(1, 51):
    site_url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    driver.get(site_url)
    books = driver.find_elements(By.CLASS_NAME, "product_pod")
    for book in books:
        book_elements = book.find_element(By.TAG_NAME, "h3")
        book_tags = book_elements.find_element(By.TAG_NAME, "a")
        book_url = book_tags.get_attribute("href")
        driver.get(book_url)
        details = driver.find_elements(By.CLASS_NAME, "row")
        for detail in details:
            main_details = detail.find_element(By.CLASS_NAME, "col-sm-6 product-main")
            title = main_details.find_element(By.TAG_NAME, "h1").text
            price = main_details.find_element(By.CLASS_NAME, "price_color").text
        scraped_data.append({
            "title": title,
            "price": price
        })
print(scraped_data)