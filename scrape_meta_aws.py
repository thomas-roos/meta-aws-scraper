#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
from packaging import version

def get_current_releases():
    url = "https://www.yoctoproject.org/development/releases/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    releases = []
    current_section = soup.find('div', id='current')
    if current_section:
        table = current_section.find('table')
        if table:
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if cols:
                    codename = cols[0].text.strip().lower()
                    if codename:
                        releases.append(codename)
    return releases

def get_recipes(branch="master"):
    url = f"https://layers.openembedded.org/layerindex/branch/{branch}/layer/meta-aws/"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    recipes = {}
    
    for row in soup.select('table.table tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            recipe = cols[0].text.strip()
            ver = cols[1].text.strip()
            if recipe and not any(month in recipe for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                recipes[recipe] = ver
    
    return recipes

def color_version(ver, versions):
    if ver == "-" or ver == "":
        return ver
    valid = [v for v in versions if v != "-" and v != ""]
    if len(set(valid)) <= 1:
        return ver
    try:
        unique = sorted(set(valid), key=lambda x: version.parse(x), reverse=True)
    except:
        return ver
    if ver == unique[0]:
        return f'<span style="color:green">**{ver}**</span>'
    elif ver == unique[-1]:
        return f'<span style="color:red">{ver}</span>'
    else:
        return f'<span style="color:orange">{ver}</span>'

def main():
    print("Fetching current Yocto releases...", file=sys.stderr)
    releases = get_current_releases()
    branches = ["master"] + releases
    print(f"Found releases: {', '.join(branches)}", file=sys.stderr)
    
    all_data = {}
    
    for branch in branches:
        try:
            print(f"Fetching {branch}...", file=sys.stderr)
            all_data[branch] = get_recipes(branch)
        except Exception as e:
            print(f"Skipping {branch}: {e}", file=sys.stderr)
            continue
    
    all_recipes = set()
    for recipes in all_data.values():
        all_recipes.update(recipes.keys())
    
    branches = list(all_data.keys())
    print("| Recipe | " + " | ".join(branches) + " |")
    print("|--------|" + "|".join(["--------"] * len(branches)) + "|")
    
    for recipe in sorted(all_recipes):
        versions = [all_data[branch].get(recipe, "-") for branch in branches]
        colored = [color_version(v, versions) for v in versions]
        print("| " + recipe + " | " + " | ".join(colored) + " |")

if __name__ == "__main__":
    main()
