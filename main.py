#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,line-too-long

import requests

data = requests.get(url="https://launchpad.binance.com/gateway-api/v1/public/launchpool/project/list", headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}).json()

# Get the assets for which a Launchpool is currently in progress.
assetsDict = dict()
assetsSet = set()
for project in data["data"]["tracking"]["list"]:
    assetsDict[project["projectId"]] = dict(project)
    assetsSet.add(project["asset"])

assetInput = input("Select your asset ({}): ".format(", ".join(sorted(assetsSet))))

# Filter the dict based on user input, sort it by highest yield, and print results.
projectsDict = sorted(assetsDict.items(), key=lambda x: x[1]["annualRate"], reverse=True)
for index, (projectKey, projectValue) in enumerate(projectsDict):
    if projectValue["asset"] == assetInput:
        name = projectKey.split("_")[0]
        apy = round(float(projectValue["annualRate"]) * 100, 2)
        print("{}. {} with {}% APY".format(index + 1, name, apy))
