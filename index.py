import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

def get_product_details(url, user_agent):
    status_code = 503

    while status_code == 503:
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            title_element = soup.find("h1", {"class": "pdp-e-i-head"}) or soup.find("span", {"id": "productTitle"})
            title = title_element.get_text().strip() if title_element else "Title not found"

            price_element = soup.find("span", {"class": "pdp-final-price"}) or soup.find("span", {"class": "a-price-whole"})
            price = price_element.get_text().strip() if price_element else "Price not found"

            image_element = soup.find("img", {"class": "cloudzoom"}) or soup.find("img", {"id": "landingImage"})
            image = image_element["src"] if image_element else "Image not found"

            description_element = soup.find("div", {"class": "col-xs-18"}) or soup.find("div", {"id": "productDescription"})
            description = description_element.get_text().strip() if description_element else "Description not found"
            status_code = 200

            return {
                "title": title,
                "price": price,
                "image": image,
                "description": description
            }
        else:
            print(f"Failed to retrieve product details. Retrying for URL: {url}")

def compare_prices(url1, url2, user_agent):
    product1_details = get_product_details(url1, user_agent)
    product2_details = get_product_details(url2, user_agent)

    try:
        product1_price = float(product1_details["price"].replace("Rs.", "").replace(",", ""))
    except ValueError:
        product1_price = float("inf")

    try:
        product2_price = float(product2_details["price"].replace("Rs.", "").replace(",", ""))
    except ValueError:
        product2_price = float("inf")

    if product2_price < product1_price:
        return product2_details, url2
    else:
        return product1_details, url1

if __name__ == "__main__":
    url1 = input("Enter the first product URL: ")
    url2 = input("Enter the second product URL: ")
    cheaper_product, product_url = compare_prices(url1, url2, USER_AGENT)

    if cheaper_product:
        table = [["Field", "Value"],
                 ["Title", cheaper_product["title"]],
                 ["Price", cheaper_product["price"]],
                 ["Image", cheaper_product["image"]],
                 ["Description", cheaper_product["description"]],
                 ["Product Link", product_url]]
        print(tabulate(table, headers='firstrow', tablefmt='grid'))
    else:
        print("Failed to retrieve product details or URLs are incorrect.")
