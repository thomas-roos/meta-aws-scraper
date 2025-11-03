#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys

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
            version = cols[1].text.strip()
            recipes[recipe] = version
    
    return recipes

def main():
    branches = ["master", "scarthgap", "nanbield", "mickledore", "langdale", "kirkstone"]
    all_data = {}
    
    for branch in branches:
        try:
            print(f"Fetching {branch}...", file=sys.stderr)
            all_data[branch] = get_recipes(branch)
        except Exception as e:
            print(f"Error fetching {branch}: {e}", file=sys.stderr)
            all_data[branch] = {}
    
    all_recipes = set()
    for recipes in all_data.values():
        all_recipes.update(recipes.keys())
    
    print("| Recipe | " + " | ".join(branches) + " |")
    print("|--------|" + "|".join(["--------"] * len(branches)) + "|")
    
    for recipe in sorted(all_recipes):
        row = [recipe]
        for branch in branches:
            row.append(all_data[branch].get(recipe, "-"))
        print("| " + " | ".join(row) + " |")

if __name__ == "__main__":
    main()
