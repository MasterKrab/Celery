from bs4 import BeautifulSoup
import requests


def get_user_agents():
    response = requests.get(
        "https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/"
    )
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.select("table td a")

    user_agents = [link.text.strip() for link in links]

    print(f"Found {len(user_agents)} user agents")

    return user_agents


user_agents = get_user_agents()
