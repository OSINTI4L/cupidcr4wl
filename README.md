<div align="center">

# 💘 cupidcr4wl 💘

**[Version 2.2](https://github.com/OSINTI4L/cupidcr4wl/releases/tag/cupidcr4wl-v2.2)**

cupidcr4wl is an open-source intelligence username and phone number search tool that crawls adult content platforms to see if a targeted account or person is present. The need for a tool of this manner derived from missing persons investigations where dating, adult video/photo platforms, and concerns of human trafficking were found relevant.

![demo](https://github.com/user-attachments/assets/e4fe1b7a-fa3e-4cf0-8321-8a926fc705c3)

cupidcr4wl searches the following platforms:

```Payment and Gifting | Social | Dating and hook-up | Fetish | Adult video and photo | Camming | Escort```

Please see the [contributing](https://github.com/OSINTI4L/cupidcr4wl/blob/main/.github/CONTRIBUTING.md) section if you find cupidcr4wl is returning false positive/negative results so it can be fixed. As web developers update site code, it is inevitabile that at some point certain results may be inaccurate. Contributing is a helpful way of alerting to these inaccuracies so they can be fixed. You can also submit a site to be added to the cupidcr4wl search list!


The site list that cupidcr4wl utilizes for searching is updated for accuracy and expanded regularly.

⚠️**WARNING**⚠️ 

cupidcr4wl **will** search and return results for platforms that host content for mature adult audiences. You are expected to use this tool in accordance with the laws and regulations in your respective jurisdiction(s). If while using cupidcr4wl you believe that you have discovered a platform hosting illegal content, you can utilize the [law enforcement reporting resources](https://github.com/OSINTI4L/cupidcr4wl/blob/main/.github/LEReportingResources.md) section to report it.

## [Installation](#installation) | [Usage](#usage) | [Contributing](https://github.com/OSINTI4L/cupidcr4wl/blob/main/.github/CONTRIBUTING.md) | [Documentation](https://github.com/OSINTI4L/cupidcr4wl/wiki)

</div>

## Requirements
- Python 3.6 or higher

  - ```requests```

  - ```rich```

## Installation

1) Clone the repository:

&nbsp;&nbsp;&nbsp;&nbsp;```git clone https://github.com/OSINTI4L/cupidcr4wl```


2) Change directories to cupidcr4wl:

&nbsp;&nbsp;&nbsp;&nbsp;```cd cupidcr4wl```


3) Install the requirements:

&nbsp;&nbsp;&nbsp;&nbsp;```pip install -r requirements.txt```

## Usage
1) To see all cupidcr4wl command line arguments:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -h``` or ```python3 cc.py --help```

```
usage: cc.py [-h] [-p PHONENUMBER] [-u USERNAME] [--export-results] [--debug]
             [--username-sites] [--phone-number-sites]

A tool for checking if a username or phone number exists across various adult content
platforms.

options:
  -h, --help            show this help message and exit
                        
  -p PHONENUMBER        Enter a phone number or multiple phone numbers (separated by commas)
                        to search.
                        
  -u USERNAME           Enter a username or multiple usernames (separated by commas) to
                        search.
                        
  --export-results      Search results will be exported to an HTML file named
                        'cc_results.html' in the current working directory.
                        
  --debug               Debug mode shows all results, HTTP response codes,
                        check_text/not_found_text matches, timeouts, and errors for each
                        site checked.
                        
  --username-sites      Prints all sites that cupidcr4wl will search by username.
                        
  --phone-number-sites  Prints all sites that cupidcr4wl will search by phone number.
```
2) To perform a search of a username:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username```

>Due to how different platforms structure their URL parameters it is recommended to run your target username in multiple different variations. E.g., ```janedoe``` ```jane_doe``` ```jane-doe``` ```jdoe```

3) To perform a search of multiple usernames simultaneously separate them by commas (with no spaces):

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username1,username2,username3```

To perform a search of a phone number:

&nbsp;&nbsp;&nbsp;&nbsp; ```python3 cc.py -p 1234567890```

>Due to how different platforms structure their URL parameters it is recommended to run your target username in multiple different variations. E.g., ```1234567890``` ```123-456-7890```

4) To perform a search of multiple phone numbers simultaneously separate them by commas (with no spaces):

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -p 1234567890,123-456-7890```

5) To export a copy of the search results to an HTML file named 'cc_results.html' in the current working directory:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username --export-results```

6) To view a list of all sites that cupidcr4wl will search by username:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py --username-sites```

7) To view a list of all sites that cupidcr4wl will search by phone number:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py --phone-number-sites```

8) To run cupidcr4wl in debug mode to test for false positives/negatives and display timeouts/errors add the ```--debug``` argument:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username --debug```

&nbsp;&nbsp;&nbsp;&nbsp;(more can be read on this mode in the [documentation](https://github.com/OSINTI4L/cupidcr4wl/wiki/Usage-Options) section)
