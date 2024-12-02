<div align="center">
  
# 🌟 Thank you for taking the time to contribute! 🌟
  
There are two main ways you can contribute sites to add to the cupidcr4wl search list or report false positive/negative results:
</div>

>**NOTE: DO NOT** submit a site that hosts illegal content to be added to cupidcr4wl, it will be ignored and removed!
  
## The easy way:
Utilize the [issues](https://github.com/OSINTI4L/cupidcr4wl/issues) tab to fill out and submit the information. I will then do all the heavy lifting of checking that the platform can be crawled by cupidcr4wl, check for accuracy, and format the platform information into the websites.json file.

The reporting of a false a positive/negative can also be submitted in this manner.

## The hard way:
Utilize a pull request to directly submit code to the [websites.json file](https://github.com/OSINTI4L/cupidcr4wl/blob/main/websites.json).

If you choose this route, the json format must follow the following syntax:

```
         },
        "Name of Platform": {
            "url": "https://www.example.com/path/to/{username}",
            "check_text": [
                "html snippets of account page"
            ],
              "not_found_text": [
                "html snippets of no account page"
            ],
            "category": "the category of the platform"
```

### Platform
Enter the name of the platform that cupidcr4wl will search:
```
},
        "Name of Platform": {
```

### URL
Enter the URL path to an account or search:

```"url": "https://www.example.com/path/to/{username}",```

### check_text
The ```check_text``` feature in cupidcr4wl parses the html of the pages it searches to look for specific html code snippets present on a valid account page. This helps with the accuracy of the tool. To parse html code:
1. Go to a valid account page.
2. Right click > View Page Source.
3. Parse and list html code snippets that are present **ONLY** on a **VALID** account page and not a non-valid account page (spoken about next).

List this information in the ```"check_text": [``` section.

Multiple html snippets can be added to this section using commas:

```
"check_text": [
  "followers",
  "subscribe",
  "profile"
],
```

### not_found_text
Inversely, not_found_text are html code snippets that are found on a **NON-VALID** account page.
1. Find an invalid account page by adding a string of random characters in the username area of the url e.g., ```https://example.com/user/sdf4657u66h4g3```.
2. You will be redirected to an "account not found page", 404 page, site landing page, or similar.
3. Right click > View Page Source.
4. Parse and list html code that is present **ONLY** on the **NON-VALID** account page.

Multiple html snippets can be added to this section using commas:
```
"not_found_text": [
  "404",
  "page not found",
  "sorry that profile doesn't exist"
],
```

You can see examples of html parsed code snippets used for the purposes of ```check_text``` and ```not_found_text``` in the [websites.json](https://github.com/OSINTI4L/cupidcr4wl/blob/main/websites.json) file.

It is important that the ```check_text``` and ```not_found_text``` are accurate as to ensure good results by cupidcr4wl. My typical workflow to ensure this is:
1. Open the page source code of a known good account.
2. Open the page source code of an invalid account page in a second tab.
3. Find unique html code snippets and use CTRL+F to ensure they are unique to each respective page by searching the snippets against the opposite pages' source code. You can also use an [html compare tool](https://www.textcompare.org/html/) to hasten and simplify the parsing.

### Category
Add the category type so that cupidcr4wl will display results to their respective categories.
The current categories are:
```
"payment and gifting"
"social"
"dating and hook-up"
"fetish"
"adult video and photo"
"camming"
"escort"
```
### Test for accuracy
Testing can be done by searching a random string of characters e.g., "safgdh543g24" and a known good account name e.g., "john" with cupidcr4wl after you have added the entry to the websites.json file. The random string of characters should return no results and the known good account should be listed as account found (or possible account found). You can also use ```--debug``` mode to receive more technical detail about the search results (shows HTTP response codes and lists ```check_text``` ```not_found_text``` results).
