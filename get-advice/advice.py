#!/usr/bin/env python3

import json
import requests
import sys


def get_advice(URL):
    session = requests.session()
    try:
        response = session.get(URL)
        data = json.loads(response.text)
        session.close()
        return data["slip"]["advice"]

    except:
        print("Bad URL, double check and try again...")
        sys.exit(1)

    finally:
        session.close()


if __name__ == "__main__":

    URL = "https://api.adviceslip.com/advice"
    advice = get_advice(URL)
    print(advice)
