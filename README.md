# I don't want to be recruited thank you very much

This repository aims at catching recruiters' communication. You can then mark it as spam, delete it, label it, or whatever else you prefer.

## Features

- The gmail filter is in the repo, click and go
- Few basic command line tools to handle the list of domains
- Filters can be imported multiple times in gmail without duplicates

# What does it do?

We have a list of Uk recruiters' domains, and an up to date xml file that can be imported into gmail filters. By default these filters will make the email skip the inbox and add a "recruitment" lebel to it.

# How do I use it?

Download the file [gmail_filter.xml](https://raw.githubusercontent.com/StefanoChiodino/i-dont-want-to-be-recruited-thank-you-very-much/master/gmail_filter.xml) and import it into gmail. Feel free to customise what each filter does.

[Google support page on how to import a filter](https://support.google.com/mail/answer/6579?hl=en-GB#zippy=%2Cexport-or-import-filters)

# How do I contribute to the list?

## Easy mode

Open an issue on [github](https://github.com/StefanoChiodino/i-dont-want-to-be-recruited-thank-you-very-much/issues/new/choose).

## DIY

### Requirements

- Python 3 installed
- git installed
- Understanding of how merge requests work

### Steps

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Add a new domain "domain.com"
python main.py add domain.com

# Update the xml gmail filter
python main.py export

# Commit changes
git commit -am "added domain.com"

# Push the changes to your repository
git push

# Open a merge request
```

# Acknowledgments

Initial list seeded from:

- https://github.com/jasoncartwright/recruiterdomains
- https://github.com/drcongo/spammy-recruiters
- https://github.com/alexmbird/uk-it-recruiter-domains
