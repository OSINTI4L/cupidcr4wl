import argparse
import json
import requests
import random
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from time import sleep
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()

ASCII_ART = r"""
          [bold cyan]_
      [bold magenta].-'` |___________________________//////
      [bold cyan]`'-._|https://github.com/OSINTI4L\\\\\\
                    [bold blue]_     __          __ __          __
  [bold cyan]_______  ______  (_)___/ /_________/ // /_      __/ /
 [bold magenta]/ ___/ / / / __ \/ / __  / ___/ ___/ // /| | /| / / / 
[bold blue]/ /__/ /_/ / /_/ / / /_/ / /__/ /  /__  __/ |/ |/ / /  
[bold cyan]\___/\__,_/ .___/_/\__,_/\___/_/ v2.2/_/  |__/|__/_/   
         [bold magenta]/_/                                            
"""

def display_ascii_art():
    """Display hardcoded ASCII art directly in the console."""
    console.print(ASCII_ART)


# --------------------------------------------------


def strip_color_tags(text):
    """Remove all color tags like [green] and [/green] from the given text."""
    while '[' in text and ']' in text:
        start = text.find('[')
        end = text.find(']', start) + 1
        text = text[:start] + text[end:]  # Remove color tags
    return text


# --------------------------------------------------


def load_websites(file_path):
    """Load website information from a JSON file and organize by category."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    categorized_websites = defaultdict(dict)
    for site, info in data['websites'].items():
        category = info.get("category", "Other")
        categorized_websites[category][site] = info
    return categorized_websites


# --------------------------------------------------


def load_user_agents(file_path):
    """Load user agents from a text file."""
    with open(file_path, 'r') as file:
        user_agents = file.read().splitlines()
    return user_agents


# --------------------------------------------------


def write_message(message, write_to_file=None, is_html=False):
    """Write message to console and optionally to a file."""
    console.print(message)
    if write_to_file:
        if is_html:
            clean_text = strip_color_tags(message)
            
            # Initialize potential_url and url_text
            potential_url = None
            
            # Look for a URL in the clean text
            for part in clean_text.split(' '):
                if part.startswith("http://") or part.startswith("https://"):
                    potential_url = part.strip() # Get the clean URL
                    break

            # 2. Convert rich text color tags to HTML spans
            html_message = message.replace("[green]", "<span style='color: green;'>") \
                                  .replace("[red]", "<span style='color: red;'>") \
                                  .replace("[yellow]", "<span style='color: orange;'>") \
                                  .replace("[cyan]", "<span style='color: cyan;'>") \
                                  .replace("[blue]", "<span style='color: blue;'>") \
                                  .replace("[magenta]", "<span style='color: magenta;'>") \
                                  .replace("[bold red]", "<span style='color: red; font-weight: bold;'>") \
                                  .replace("[bold cyan]", "<span style='color: cyan; font-weight: bold;'>") \
                                  .replace("[bold blue]", "<span style='color: blue; font-weight: bold;'>") \
                                  .replace("[bold green]", "<span style='color: green; font-weight: bold;'>") \
                                  .replace("[bold magenta]", "<span style='color: magenta; font-weight: bold;'>") \
                                  .replace("[/green]", "</span>") \
                                  .replace("[/red]", "</span>") \
                                  .replace("[/yellow]", "</span>") \
                                  .replace("[/cyan]", "</span>") \
                                  .replace("[/blue]", "</span>") \
                                  .replace("[/magenta]", "</span>")

            if potential_url:
                html_message = html_message.replace(potential_url, f"<a href='{potential_url}' target='_blank'>{potential_url}</a>")

            write_to_file.write(f"<p>{html_message}</p>\n")

# --------------------------------------------------


def check_single_site(username, site, info, user_agents, write_to_file=None, debug=False, is_html=False):
    """Check a single site for the username."""
    url = info.get("url").format(username=username)
    check_texts = info.get("check_text", [])
    not_found_texts = info.get("not_found_text", [])
    
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    if not url or not check_texts:
        write_message(f"[yellow]Skipping {site}: URL or check text missing.[/yellow]", write_to_file, is_html)
        return False

    # Optional POST support for sites that search via a form submission.
    method = info.get("method", "GET").upper()
    post_data = info.get("data")
    if isinstance(post_data, dict):
        post_data = {key: str(value).format(username=username) for key, value in post_data.items()}

    try:
        if method == "POST":
            response = requests.post(url, headers=headers, data=post_data, timeout=5)
        else:
            response = requests.get(url, headers=headers, timeout=5)
        response_code = f" (Response code: {response.status_code})" if debug else ""
        
        # Identify which specific texts matched
        matching_check_texts = [check_text for check_text in check_texts if check_text.lower() in response.text.lower()]
        matching_not_found_texts = [not_found_text for not_found_text in not_found_texts if not_found_text.lower() in response.text.lower()]

        # Determine the status and construct the appropriate message
        if response.status_code == 200:
            if matching_check_texts:
                message = f"[green]↳ Account found on {site}: {url}{response_code}[/green]"
                if debug:
                    matched_items = ", ".join(matching_check_texts)
                    message += f" [cyan](Matched check_text items: {matched_items})[/cyan]"
            elif matching_not_found_texts:
                message = f"[red]✗ No account found on {site}.{response_code}[/red]"
                if debug:
                    matched_items = ", ".join(matching_not_found_texts)
                    message += f" [cyan](Matched not_found_text items: {matched_items})[/cyan]"
            else:
                message = f"[yellow]↳ Possible account found on {site}: {url}{response_code}[/yellow]"
        else:
            message = f"[red]✗ No account found on {site}.{response_code}[/red]"
            if debug and matching_not_found_texts:
                matched_items = ", ".join(matching_not_found_texts)
                message += f" [cyan](Matched not_found_text items: {matched_items})[/cyan]"

    except requests.Timeout:
        message = f"[bold red]✗ Timeout while checking {site}.[/bold red]"
    except requests.RequestException as e:
        message = f"[bold red]✗ Network error checking {site}: {str(e)}.[/bold red]"

    found = "[green]" in message or "[yellow]" in message
    if debug or found:
        write_message(message, write_to_file, is_html)
    return found


# --------------------------------------------------


def print_category_header(category, write_to_file=None, is_html=False):
    """Print and optionally write category header."""
    message = f"\n[bold blue]💘Results for {category} platforms💘[/bold blue]"
    console.print(message) # <--- ADD THIS LINE BACK TO ALWAYS PRINT TO CONSOLE
    if write_to_file and is_html:
        write_to_file.write(f"<h2>{strip_color_tags(message)}</h2>\n")


# --------------------------------------------------


def check_usernames(usernames, user_agents, write_to_file=None, debug=False, use_phone_numbers=False, is_html=False):
    """Check the provided usernames or phone numbers across various websites."""
    if use_phone_numbers:
        websites_by_category = load_websites('phonenumbers.json')  # Load phone numbers file
    else:
        websites_by_category = load_websites('usernames.json')  # Load normal websites file

    # Outer loop for each username
    for username in usernames:
        # Write username header to the results file, if applicable
        if write_to_file:
            if is_html:
                write_to_file.write(f"<h1>Results for {username}:</h1>\n")  # Add a header for the username in the file
            else:
                write_to_file.write(f"\nResults for {username}:\n")  # Add a header for the username in the file

        console.print(f"[bold cyan]Checking: {username}[/bold cyan]")  # Print username being checked
        
        with Progress(
            SpinnerColumn(style="bold cyan"),
            BarColumn(bar_width=None, complete_style="magenta"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("{task.description}"),
            console=console
        ) as progress:

            total_sites = sum(len(sites) for sites in websites_by_category.values())
            overall_task = progress.add_task(f"[bold magenta]Checking {username}...", total=total_sites)

            for category, sites in websites_by_category.items():
                print_category_header(category, write_to_file, is_html)

                category_had_hit = False
                with ThreadPoolExecutor(max_workers=8) as executor:
                    future_to_site = {
                        executor.submit(check_single_site, username.strip(), site, info, user_agents, write_to_file, debug, is_html): site
                        for site, info in sites.items()
                    }
                    for future in as_completed(future_to_site):
                        site = future_to_site[future]
                        try:
                            if future.result():
                                category_had_hit = True
                        except Exception as e:
                            write_message(f"[bold red]Error checking {site}: {e}[bold red]", write_to_file, is_html)

                        progress.update(overall_task, advance=1)  # Advance the task for the overall progress
                        sleep(0.2)

                # Normal mode only: flag categories that returned nothing (debug already lists every site)
                if not category_had_hit and not debug:
                    write_message(f"[red]✗ No results found.[/red]", write_to_file, is_html)

            progress.update(overall_task, completed=total_sites)  # Mark the task as completed after finishing all sites





class SpacingHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter for argparse to add spacing."""
    def _split_lines(self, text, width):
        lines = super()._split_lines(text, width)
        lines.append('')  # Add a blank line for spacing
        return lines


# --------------------------------------------------


def print_sites(file_path='usernames.json'):
    """Print all site names and their URLs from the specified JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Determine if websites or phone numbers
            if 'websites' in data:
                console.print("\n[bold blue]Sites and URLs searched by cupidcr4wl:[/bold blue]")
                for site, info in data['websites'].items():
                    url = info.get("url", "No URL available")
                    console.print(f"- {site}: {url}")
            
            elif 'phone_numbers' in data:  # Correct indentation here
                console.print("\n[bold blue]Sites and URLs searched by cupidcr4wl (Phone Numbers):[/bold blue]")
                for site, info in data['phone_numbers'].items():  # Correct indentation here
                    url = info.get("url", "No URL available")
                    console.print(f"- {site}: {url}")
            else:
                console.print(f"[bold red]Invalid or unrecognized JSON structure in {file_path}[/bold red]")

    except FileNotFoundError:
        console.print(f"[bold red]{file_path} file not found![/bold red]")
    except json.JSONDecodeError:
        console.print(f"[bold red]Error decoding JSON from {file_path}![/bold red]")


# --------------------------------------------------



def parse_arguments():
    """Parse command-line arguments for the script."""
    parser = argparse.ArgumentParser(
        description="A tool for checking if a username or phone number exists across various adult content platforms.",
        formatter_class=SpacingHelpFormatter
    )

    parser.add_argument(
        "-p",
        type=str,
        required=False,
        help="Enter a phone number or multiple phone numbers (separated by commas) to search.",
        metavar="PHONENUMBER"
    )

    parser.add_argument(
        "-u",
        type=str,
        required=False,
        help="Enter a username or multiple usernames (separated by commas) to search.",
        metavar="USERNAME"
    )

    parser.add_argument(
        "--export-results",
        action="store_true",
        help="Search results will be exported to an HTML file named 'cc_results.html' in the current working directory."
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debug mode shows all results, HTTP response codes, check_text/not_found_text matches, timeouts, and errors for each site checked."
    )

    parser.add_argument(
        "--username-sites",
        action="store_true",
        help="Prints all sites that cupidcr4wl will search by username."
    )

    parser.add_argument(
        "--phone-number-sites",
        action="store_true",
        help="Prints all sites that cupidcr4wl will search by phone number."
    )

    return parser.parse_args()


# --------------------------------------------------


def main():
    """Main entry point for the script."""
    display_ascii_art()  # Show ASCII art
    args = parse_arguments()  # Parse command-line arguments

    # Check if no arguments are provided
    if not (args.u or args.p or args.username_sites or args.phone_number_sites or args.export_results):
        console.print("[bold red]Error: Username or phone number and arguments required, see -h or --help.[/bold red]")
        return  # Return if no arguments are provided

    user_agents = load_user_agents('user_agents.txt')  # Load user agents from file

    # --export-results to export search results to a file
    write_to_file = None  # Initialize the file variable
    is_html_export = False
    if args.export_results:
        result_file_name = 'cc_results.html'  # Create the result file name for HTML
        write_to_file = open(result_file_name, 'w', encoding='utf-8')  # Open file for writing results
        is_html_export = True
        # Write HTML boilerplate and styles
        write_to_file.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CupidCr4wl Results</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #1a1a1a; color: #f0f0f0; }
        h1 { color: #00bcd4; border-bottom: 2px solid #00bcd4; padding-bottom: 10px; margin-top: 30px; }
        h2 { color: #9c27b0; margin-top: 20px; }
        p { margin: 5px 0; }
        span.green { color: green; }
        span.red { color: red; }
        span.orange { color: orange; }
        span.cyan { color: cyan; }
        span.blue { color: blue; }
        span.magenta { color: magenta; }
        a { color: #00bcd4; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>CupidCr4wl Search Results</h1>
""")

    try:
        # Check if --username-sites or --phone-number-sites is set
        if args.username_sites:  # If --username-sites is set
            print_sites('usernames.json')  # Call print_sites for usernames.json
        elif args.phone_number_sites:  # If --phone-number-sites is set
            print_sites('phonenumbers.json')  # Call print_sites for phonenumbers.json
        elif args.p:  # If phone numbers are provided, search for phone numbers
            check_usernames(args.p.split(","), user_agents, write_to_file, args.debug, use_phone_numbers=True, is_html=is_html_export)  # Only phone number search
        elif args.u:  # If usernames are provided, search for usernames
            check_usernames(args.u.split(","), user_agents, write_to_file, args.debug, use_phone_numbers=False, is_html=is_html_export)  # Only username search

        # If export_results is enabled, print success message
        if args.export_results:
            console.print(f"[bold cyan]✔ Results have been saved to '{result_file_name}'[/bold cyan]")

    finally:
        if write_to_file:
            if is_html_export:
                write_to_file.write("</body>\n</html>")
            write_to_file.close()  # Close the file if it was opened

    console.print("\n[bold cyan]💰Search complete, enjoy your[/bold cyan] [bold green]loot..💰[/bold green]")



# --------------------------------------------------


if __name__ == "__main__":
    main()  # Call the main function to run the script
