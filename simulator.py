import pandas as pd
import time
import requests
import random

def getBottom():
    url = "https://hackkosice2022.azurewebsites.net/api/v1/getGlobalDataBottom"

    payload = {}
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, json=payload, headers=headers)
    
    sample = response.json()[random.randint(0, 4)]['gameId']
    return sample

def getTop():
    url = "https://hackkosice2022.azurewebsites.net/api/v1/getGlobalDataTop"

    payload = {}
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, json=payload, headers=headers)
    sample = response.json()[random.randint(0, 4)]['gameId']
    return sample

def main():

    df = pd.read_csv("KNN_dataset.csv")
    mutex = 1
    buycounter = 0;

    while (1):
        # select random from dataset
        if mutex == 1:
            sample = df.sample(1)['product_id'].values[0]
        elif mutex == 2:
            sample = getBottom()
        else:
            sample = getTop()
            mutex = 0
        mutex += 1
        # call api      
        url = "https://hackkosice2022.azurewebsites.net/api/v1/createPrediction"
        payload = {"gameId": sample}
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, json=payload, headers=headers)

        print(f"ID - {sample} ->  result - {response}")
        # sleep
        if buycounter > 10:
            url = "https://hackkosice2022.azurewebsites.net/api/v1/updateBuy"
            payload = {"gameId": sample}
            headers = {"Content-Type": "application/json"}
            response = requests.request("POST", url, json=payload, headers=headers)

            print(f"BUY: ID - {sample} ->  result - {response}")
            buycounter = 0

        time.sleep(2)

if __name__ == "__main__":
    main()