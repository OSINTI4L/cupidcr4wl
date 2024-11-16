<div align="center">

# 💘 cupidcr4wl 💘
version 1.1

cupidcr4wl is an Open-Source Intelligence username search tool that crawls adult content platforms to see if a targeted account or person is present. The need for a tool of this manner derived from missing persons investigations where dating, adult video/photo platforms, and concerns of human trafficking were found relevant.

![demo](https://github.com/user-attachments/assets/1506cab0-11b4-45a7-a3a6-38ddd897691b)

cupidcr4wl searches the following platforms:

**Adult video, photo, and camming platforms | Dating, hook-up, and social platforms | Escort service platforms**

Please see the [contributing](https://github.com/OSINTI4L/cupidcr4wl/blob/main/.github/CONTRIBUTING.md) section if you find cupidcr4wl is returning false positive/negative results so it can be fixed. You can also submit a site to add to the cupidcr4wl search list!


The site list that cupidcr4wl utilizes for searching is updated for accuracy and expanded regularly.

⚠️**WARNING**⚠️ 

cupidcr4wl **will** search and return results for platforms that host content for mature adult audiences. You are expected to use this tool in accordance with the laws and regulations in your respective jurisdiction(s). If while using cupidcr4wl you believe that you have discovered a platform hosting illegal content, you can utilize the [law enforcement reporting resources](https://github.com/OSINTI4L/cupidcr4wl/blob/main/LEReportingResources.md) section to report it.

## [Installation](#installation) | [Usage](#usage) | [Contributing](https://github.com/OSINTI4L/cupidcr4wl/blob/main/.github/CONTRIBUTING.md) | [Documentation](https://github.com/OSINTI4L/cupidcr4wl/wiki)

</div>

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
usage: cc.py [-h] [-u USERNAME] [--export-results] [--debug] [--sites] [--export-sites]

A tool for checking if an account exists across various websites.

options:
  -h, --help        show this help message and exit
                    
  -u USERNAME       Enter a username or multiple usernames (separated by commas) to search.
                    
  --export-results  Search results will be exported to a text file named 'cc_results.txt' in
                    the current working directory.
                    
  --debug           Debug mode, shows HTTP response codes and check_text/not_found_text
                    matches for each site checked.
                    
  --sites           Print all sites that cupidcr4wl will search.
                    
  --export-sites    Export the list of sites that cupidcr4wl will search to a text file
                    named 'cc_sitelist.txt' in the current working directory.
```
2) To perform a search of a username:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username```

3) To perform a search of multiple usernames:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username1,username2,username3```

4) To export a copy of the search results to a text named 'cc_results.txt' in the current working directory:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username --export-results```

5) To view a list of all sites that cupidcr4wl will search:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py --sites```

6) To export the list of all sites that cupidcr4wl will search to a text file named "cc_sitelist.txt" in the current working directory:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py --export-sites```

7) To run cupidcr4wl in debug mode to test for false positives/negatives:

&nbsp;&nbsp;&nbsp;&nbsp;```python3 cc.py -u username --debug```

&nbsp;&nbsp;&nbsp;&nbsp;(more can be read on this mode in the [documentation](https://github.com/OSINTI4L/cupidcr4wl/wiki))

By default, cupidcr4wl will only display "Account found" and "Possible account found" results. If no account was found it will not be displayed. The --debug argument allows the user to see the "No account found" results if needed. This is done intentionally to reduce the "spaminess" of the results.
