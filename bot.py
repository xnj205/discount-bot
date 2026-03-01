from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time

# ----- CONFIG -----
TELEGRAM_TOKEN = "AAFoC0VWUIlbtcp6UmSQhgRPY9nQn9t_xYI"
CHAT_ID = 8771862194  # Your personal chat ID

URLS = {
    "Blinkit Groceries": "https://blinkit.com/cn/grocery",
    "Blinkit Fruits": "https://blinkit.com/cn/fruits-vegetables",
    "Instamart Groceries": "https://www.swiggy.com/instamart/category/grocery",
    "Instamart Fruits": "https://www.swiggy.com/instamart/category/fruits-vegetables"
}

# ----- FUNCTION TO SEND TELEGRAM ALERT -----
def send_alert(app, mrp, price, discount, product_name=""):
    message = f"🔥 40%+ OFF!\nApp: {app}\nProduct: {product_name}\nMRP: ₹{mrp}\nPrice: ₹{price}\nDiscount: {round(discount,1)}%"
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": message})

# ----- FUNCTION TO CHECK PAGE -----
def check_page(driver, name, url):
    driver.get(url)
    time.sleep(5)  # wait for page load
    
    elements = driver.find_elements(By.XPATH, "//*[contains(text(),'₹')]")
    prices = []

    for el in elements:
        text = el.text.replace("₹","").strip()
        if text.isdigit():
            prices.append(int(text))
    
    # Pair MRP and selling price
    for i in range(0, len(prices)-1, 2):
        mrp = prices[i]
        price = prices[i+1]
        if mrp > 0:
            discount = ((mrp - price)/mrp)*100
            if discount >= 70:
                send_alert(name, mrp, price, discount)

# ----- MAIN FUNCTION -----
def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    for name, url in URLS.items():
        check_page(driver, name, url)

    driver.quit()

if __name__ == "__main__":
    main()
