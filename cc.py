import argparse
import json
import requests
import random
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from time import sleep
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize the console for rich text output
console = Console()

ASCII_ART = r"""
          [bold cyan]_
      [bold magenta].-'` |___________________________//////
      [bold cyan]`'-._|https://github.com/OSINTI4L\\\\\\
                    [bold blue]_     __          __ __          __
  [bold cyan]_______  ______  (_)___/ /_________/ // /_      __/ /
 [bold magenta]/ ___/ / / / __ \/ / __  / ___/ ___/ // /| | /| / / / 
[bold blue]/ /__/ /_/ / /_/ / / /_/ / /__/ /  /__  __/ |/ |/ / /  
[bold cyan]\___/\__,_/ .___/_/\__,_/\___/_/     /_/  |__/|__/_/   
         [bold magenta]/_/                                            
"""

def display_ascii_art():
    """Display hardcoded ASCII art directly in the console."""
    console.print(ASCII_ART)

def strip_color_tags(text):
    """Remove all color tags like [green] and [/green] from the given text."""
    while '[' in text and ']' in text:
        start = text.find('[')
        end = text.find(']', start) + 1
        text = text[:start] + text[end:]  # Remove color tags
    return text

def load_websites(file_path):
    """Load website information from a JSON file and organize by category."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    categorized_websites = defaultdict(dict)
    for site, info in data['websites'].items():
        category = info.get("category", "Other")
        categorized_websites[category][site] = info
    return categorized_websites

def load_user_agents(file_path):
    """Load user agents from a text file."""
    with open(file_path, 'r') as file:
        user_agents = file.read().splitlines()
    return user_agents

def write_message(message, write_to_file=None):
    """Write message to console and optionally to a file."""
    console.print(message)
    if write_to_file:
        write_to_file.write(strip_color_tags(message) + "\n")

def check_single_site(username, site, info, user_agents, write_to_file=None, debug=False):
    """Check a single site for the username."""
    url = info.get("url").format(username=username)
    check_texts = info.get("check_text", [])
    not_found_texts = info.get("not_found_text", [])
    
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    if not url or not check_texts:
        write_message(f"[yellow]Skipping {site}: URL or check text missing.[/yellow]", write_to_file)
        return

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response_code = f" (Response code: {response.status_code})" if debug else ""
        
        # Identify which specific texts matched
        matching_check_texts = [check_text for check_text in check_texts if check_text.lower() in response.text.lower()]
        matching_not_found_texts = [not_found_text for not_found_text in not_found_texts if not_found_text.lower() in response.text.lower()]

        # Determine the status and construct the appropriate message
        if response.status_code == 200:
            if matching_check_texts:
                message = f"[green]Account found on {site}: {url}{response_code}[/green]"
                if debug:
                    matched_items = ", ".join(matching_check_texts)
                    message += f" [cyan](Matched check_text items: {matched_items})[/cyan]"
            elif matching_not_found_texts:
                message = f"[red]No account found on {site}.{response_code}[/red]"
                if debug:
                    matched_items = ", ".join(matching_not_found_texts)
                    message += f" [cyan](Matched not_found_text items: {matched_items})[/cyan]"
            else:
                message = f"[yellow]Possible account found on {site}: {url}{response_code}[/yellow]"
        else:
            message = f"[red]No account found on {site}.{response_code}[/red]"
            if debug and matching_not_found_texts:
                matched_items = ", ".join(matching_not_found_texts)
                message += f" [cyan](Matched not_found_text items: {matched_items})[/cyan]"

    except requests.Timeout:
        message = f"[bold red]Timeout while checking {site}.[/bold red]"
    except requests.RequestException as e:
        message = f"[bold red]Network error checking {site}: {str(e)}.[/bold red]"

    # Simplified message writing logic
    write_message(message, write_to_file) if debug or "[green]" in message or "[yellow]" in message else None


def print_category_header(category, write_to_file=None):
    """Print and optionally write category header."""
    message = f"\n[bold blue]Checking {category} platforms:[/bold blue]"
    write_message(message, write_to_file)

def check_usernames(usernames, user_agents, write_to_file=None, debug=False):
    """Check the provided usernames across various websites."""
    websites_by_category = load_websites('websites.json')

    # Outer loop for each username
    for username in usernames:
        # Write username header to the results file, if applicable
        if write_to_file:
            write_to_file.write(f"\nResults for {username}:\n")  # Add a header for the username in the file

        console.print(f"\n[bold cyan]Checking username: {username}[/bold cyan]")  # Print username being checked
        
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
                print_category_header(category, write_to_file)

                with ThreadPoolExecutor(max_workers=4) as executor:
                    future_to_site = {
                        executor.submit(check_single_site, username.strip(), site, info, user_agents, write_to_file, debug): site 
                        for site, info in sites.items()
                    }
                    for future in as_completed(future_to_site):
                        site = future_to_site[future]
                        try:
                            future.result()
                        except Exception as e:
                            write_message(f"[bold red]Error checking {site}: {e}[/bold red]", write_to_file)

                        progress.update(overall_task, advance=1)  # Advance the task for the overall progress
                        sleep(0.2)

            progress.update(overall_task, completed=total_sites)  # Mark the task as completed after finishing all sites



class SpacingHelpFormatter(argparse.HelpFormatter):
    """Custom help formatter for argparse to add spacing."""
    def _split_lines(self, text, width):
        lines = super()._split_lines(text, width)
        lines.append('')  # Add a blank line for spacing
        return lines

def print_sites(file_path='websites.json'):
    """Print all site names and their URLs from the JSON file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            console.print("\n[bold blue]Sites and URLs searched by cupidcr4wl:[/bold blue]")
            for site, info in data['websites'].items():
                url = info.get("url", "No URL available")
                console.print(f"- {site}: {url}")
    except FileNotFoundError:
        console.print("[bold red]websites.json file not found![/bold red]")
    except json.JSONDecodeError:
        console.print("[bold red]Error decoding JSON from websites.json![/bold red]")

def export_sites(file_path='websites.json'):
    """Export all site names and their URLs from the JSON file to 'cc_sitelist.txt'."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Open 'cc_sitelist.txt' for writing
            with open('cc_sitelist.txt', 'w') as file_output:
                for site, info in data['websites'].items():
                    url = info.get("url", "No URL available")
                    message = f"- {site}: {url}"
                    file_output.write(message + "\n")
        
        # Print a success message to the console
        console.print("[bold cyan]Site list has been exported to the current working directory as: cc_sitelist.txt[/bold cyan]")

    except FileNotFoundError:
        console.print("[bold red]websites.json file not found![/bold red]")
    except json.JSONDecodeError:
        console.print("[bold red]Error decoding JSON from websites.json![/bold red]")

def parse_arguments():
    """Parse command-line arguments for the script."""
    parser = argparse.ArgumentParser(
        description="A tool for checking if an account exists across various websites.",
        formatter_class=SpacingHelpFormatter
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
        help="Search results will be exported to a text file named 'cc_results.txt'."
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debug mode, shows HTTP response codes and check_text/not_found_text matches for each site checked."
    )

    parser.add_argument(
        "--sites",
        action="store_true",
        help="Print all sites that cupidcr4wl will check."
    )

    parser.add_argument(
        "--export-sites",
        action="store_true",
        help="Export the list of sites and their URLs to a file named 'cc_sitelist.txt' in the current working directory."
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the script."""
    display_ascii_art()  # Show ASCII art
    args = parse_arguments()  # Parse command-line arguments

    # Check if no usernames are provided and print usage information
    if args.u is None and not args.sites and not args.export_sites:
        console.print("[bold red]Error: Username and arguments required, see -h or --help.[/bold red]")
        return

    user_agents = load_user_agents('user_agents.txt')  # Load user agents from file

    # Export site list to a file if --export-sites is specified
    if args.export_sites:
        export_sites()
        return  # Exit after exporting sites

    # Print site list to the console if --sites is specified
    if args.sites:
        print_sites()
        return

    usernames = args.u.split(",") if args.u else []  # Split usernames by comma if provided

    # Check usernames and handle result file writing
    write_to_file = None  # Initialize the file variable

    if args.export_results and usernames:
        result_file_name = f'cc_results.txt'  # Create the result file name
        write_to_file = open(result_file_name, 'w')  # Open file only if conditions are met

    try:
        check_usernames(usernames, user_agents, write_to_file, args.debug)  # Check usernames
        # Print a message indicating results have been saved if exporting is enabled
        if args.export_results and usernames:
            console.print(f"[bold cyan]Results have been saved to '{result_file_name}'[/bold cyan]")
    finally:
        if write_to_file:
            write_to_file.close()  # Close the file if it was opened


if __name__ == "__main__":
    main()  # Call the main function to run the script

