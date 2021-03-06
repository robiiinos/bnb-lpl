#!/usr/bin/env python3

import requests
import shadow_useragent

URL = "https://launchpad.binance.com/gateway-api/v1/public/launchpool/project/list"  # nopep8
data = requests.get(
    url=URL,
    headers={
        "Accept": "application/json",
        "User-Agent": shadow_useragent.ShadowUserAgent().most_common
    }
).json()

# Filter projects that are available (aka "MINING"), with an annual rate (APY).
projects = filter(
    lambda elem: elem["status"] == "MINING" and elem["annualRate"] is not None,
    data["data"]["tracking"]["list"]
)

# Get assets for which a Launchpool is currently in progress.
assetsDict = dict()
assetsSet = set()
for project in projects:
    assetsDict[project["projectId"]] = dict(project)
    assetsSet.add(project["asset"])

ASSET_INPUT = ""
while ASSET_INPUT.upper() not in assetsSet:
    # Fetch user input for asset, and set default if none.
    ASSET_INPUT = input(
        "Select your asset ({}): ".format(
            ", ".join(sorted(assetsSet))
        )
    ) or "BNB"

    # 1. Filter dict based on user input
    # 2. Sort dict by highest yield
    projectsDict = filter(
        lambda elem: elem[1]["asset"] == ASSET_INPUT.upper(),
        sorted(
            assetsDict.items(),
            key=lambda elem: elem[1]["annualRate"],
            reverse=True
        )
    )

    # Print results.
    for index, key in enumerate(projectsDict):
        name = key[0].split("_")[0]
        apy = round(float(key[1]["annualRate"]) * 100, 2)
        print("{}. {} with {}% APY".format(index + 1, name, apy))
