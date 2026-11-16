import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
)
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def check_train_delay(line: str) -> None:
    r = session.get(
        "https://api.golemio.cz/v2/vehiclepositions/",
        headers={"x-access-token": "YOUR API KEY FOR GOLEMIO"},
        params={"routeId": "YOUR ROUTE ID DEPENDENT ON THE LINE YOU NEED TO TRACK"},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()

    my_train = "not found"
    my_delay = "not found"
    for feature in data["features"]:
        props = feature["properties"]
        if props["trip"]["gtfs"]["trip_short_name"] == line:
            my_train = line
            delay = props["last_position"]["delay"]["actual"]
            if delay is not None:
                my_delay = delay // 60
            break

    try:
        r = session.post(
            f"https://ntfy.sh/YOUR_DESIGNED_ENDPOINT",
            data=f"Linka: {my_train}, zpoždění: {my_delay} min".encode("utf-8"),
            timeout=30,
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error("Could not send notification: %s", e)

check_train_delay("YOUR LINE")

