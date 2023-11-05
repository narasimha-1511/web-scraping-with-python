import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"


def get_product_details_snapdeal(url, user_agent):
    status_code = 503

    while status_code == 503:
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            title_element = soup.find("h1", {"class": "pdp-e-i-head"})
            title = title_element.get_text().strip() if title_element else "Title not found"

            price_element = soup.find("span", {"class": "pdp-final-price"})
            price = price_element.get_text().strip() if price_element else "Price not found"

            image_element = soup.find("img", {"class": "cloudzoom"})
            image = image_element["src"] if image_element else "Image not found"

            description_element = soup.find("div", {"class": "col-xs-18"})
            description = description_element.get_text().strip() if description_element else "Description not found"
            status_code = 200

            return {
                "title": title,
                "price": price,
                "image": image,
                "description": description
            }
        else:
            print("Failed to retrieve Snapdeal product details. Retrying...")


def get_product_details_amazon(url, user_agent):
    status_code = 503

    while status_code == 503:
        headers = {"User-Agent": user_agent}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            title_element = soup.find("span", {"id": "productTitle"})
            title = title_element.get_text().strip() if title_element else "Title not found"

            price_element = soup.find("span", {"class": "a-price-whole"})
            price = price_element.get_text().strip() if price_element else "Price not found"

            image_element = soup.find("img", {"id": "landingImage"})
            image = image_element["src"] if image_element else "Image not found"

            description_element = soup.find("div", {"id": "productDescription"})
            description = description_element.get_text().strip() if description_element else "Description not found"
            status_code = 200

            return {
                "title": title,
                "price": price,
                "image": image,
                "description": description
            }
        else:
            print("Failed to retrieve Amazon product details. Retrying...")
    

def compare_prices(url_snapdeal, url_amazon):
    snapdeal_details = get_product_details_snapdeal(url_snapdeal, user_agent)
    amazon_details = get_product_details_amazon(url_amazon, user_agent)

    try:
        snapdeal_price = float(snapdeal_details["price"].replace("Rs.", "").replace(",", ""))
    except ValueError:
        snapdeal_price = float("inf")

    try:
        amazon_price = float(amazon_details["price"].replace("Rs.", "").replace(",", ""))
    except ValueError:
        amazon_price = float("inf")


    if amazon_price < snapdeal_price:
        return amazon_details, url_amazon
    else:
        return snapdeal_details, url_snapdeal

    return None, None


if __name__ == "__main__":
    snapdeal_url = input("Enter Snapdeal Product Link:")
    amazon_url = input("Enter amazon Product Link:")
    cheaper_product, product_url = compare_prices(snapdeal_url, amazon_url)

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