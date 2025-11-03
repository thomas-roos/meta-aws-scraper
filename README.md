# meta-aws Recipe Scraper

Scrapes recipe versions from the OpenEmbedded meta-aws layer across different releases.

## Usage

```bash
pip install -r requirements.txt
python scrape_meta_aws.py > recipes.md
```

## GitHub Actions

The workflow runs weekly and on manual trigger, generating a markdown table of all recipes and their versions across releases.
