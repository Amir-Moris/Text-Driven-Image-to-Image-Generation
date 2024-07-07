import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def scrap(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    div_elements = soup.find_all("div", class_="WxXog")
    result = []
    for div in div_elements:
        img_tag = div.find("img")
        if img_tag:
            alt_text = img_tag.get("alt")
            if alt_text is not None and len(alt_text) < 100:
                result.append(alt_text)

    return result


def main():
    data = []

    categories = [
        "shoes",
        "sneakers",
        "heels",
        "watches",
        "pants",
        "clothing",
        "dress",
        "shirt",
        "t-shirt",
    ]
    seen_inputs = set()
    base_url = "https://unsplash.com/s/photos/"

    for category in categories:
        url = f"{base_url}{category}"
        print(f"Scraping {url}...")
        res = scrap(url)
        if res is not None:
            for t in res:
                if t not in seen_inputs:
                    data.append({"category": category, "caption": t})
                    seen_inputs.add(t)

        time.sleep(1)  # Delay to avoid rate limiting

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv("input_dataset.csv", index=False)


if __name__ == "__main__":
    main()
