#!/usr/bin/env python3
# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,line-too-long

import requests
import shadow_useragent

data = requests.get(url="https://launchpad.binance.com/gateway-api/v1/public/launchpool/project/list", headers={
    "Accept": "application/json",
    "User-Agent": shadow_useragent.ShadowUserAgent().most_common
}).json()

# Get the assets for which a Launchpool is currently in progress.
assetsDict = dict()
assetsSet = set()
for project in data["data"]["tracking"]["list"]:
    assetsDict[project["projectId"]] = dict(project)
    assetsSet.add(project["asset"])

ASSET_INPUT = ""
while ASSET_INPUT.upper() not in assetsSet:
    ASSET_INPUT = input("Select your asset ({}): ".format(", ".join(sorted(assetsSet)))) or "BNB"

    # Filter the dict based on user input, sort it by highest yield, and print results.
    projectsDict = filter(
        lambda elem: elem[1]['asset'] == ASSET_INPUT,
        sorted(assetsDict.items(), key=lambda x: x[1]["annualRate"], reverse=True)
    )

    for index, key in enumerate(projectsDict):
        name = key[0].split("_")[0]
        apy = round(float(key[1]["annualRate"]) * 100, 2)
        print("{}. {} with {}% APY".format(index, name, apy))
