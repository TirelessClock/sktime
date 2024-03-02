import requests
from datetime import datetime, timedelta

def fetch_contributors(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
    response = requests.get(url)
    contributors_data = response.json()
    return contributors_data

def calculate_top_contributors(data):
    k = 3
    sorted_contributors = sorted(data, key=lambda x: x['total'], reverse=True)
    top_contributors = sorted_contributors[:k]
    return top_contributors

def calculate_new_contributors(data):
    k = 3
    first_contribution = {}

    for contributor in data:
        for week in contributor['weeks']:
            if week['c'] != 0:
                first_contribution[data.index(contributor)] = week["w"]
                break
    
    sorted_contributors = sorted(first_contribution.items(), key=lambda x: x[1], reverse=True)
    newest_contributors = [data[contributor] for contributor, _ in sorted_contributors[:k]]
    return newest_contributors

def analyze_contributions(contributors_data):
    top_contributors = []
    new_contributors = []

    top_contributors = calculate_top_contributors(contributors_data)
    new_contributors = calculate_new_contributors(contributors_data)

    return top_contributors, new_contributors

def display(top_contributors, new_contributors): 
    
    widget_template = (
        '<div style="display: inline-block; margin-right: 10px;">'
        '<a href="{profile_url}">'
        '<img src="{avatar_url}" alt="{username}" title="{username}" width="100" height="100" style="border-radius: 100%; border: 3px solid {border_color};">'
        '</a>'
        '<p style="text-align: center;">{username}</p>'
        '</div>'
    )

    widgets = []

    for contributor in top_contributors: 
        widget = widget_template.format(
            profile_url=contributor["author"]["html_url"], 
            avatar_url=contributor["author"]["avatar_url"], 
            username=contributor["author"]["login"],
            border_color="blue"
        )
        widgets.append(widget)

    for contributor in new_contributors: 
        widget = widget_template.format(
            profile_url=contributor["author"]["html_url"], 
            avatar_url=contributor["author"]["avatar_url"], 
            username=contributor["author"]["login"],
            border_color="green"
        )
        widgets.append(widget)

    return widgets


def main():
    owner = "TirelessClock"
    repo = "sktime"
    
    contributors_data = fetch_contributors(owner, repo)

    top_contributors, new_contributors = analyze_contributions(contributors_data)
    
    widgets = display(top_contributors, new_contributors)

    # Combine widgets into a single HTML string
    widgets_stuff = '\n'.join(widgets)

    widgets_html = f'<div style = "background-color: green"> {widgets_stuff} </div>'

    # Read existing contents of the README file
    with open("README.md", "r") as file:
        readme_contents = file.read()

    # Define the start and end markers for the section to update
    start_marker = "## Contributors' Hall of Fame"
    end_marker = "<!--END_CONTRIBUTORS_WIDGET-->"

    # Find the start and end positions of the section to update
    start_pos = readme_contents.find(start_marker)
    end_pos = readme_contents.find(end_marker, start_pos + len(start_marker))

    # If the section exists, replace it with the updated information
    if start_pos != -1 and end_pos != -1:
        updated_section = f"{start_marker}\n{widgets_html}\n"
        updated_contents = (
            readme_contents[:start_pos]
            + updated_section
            + readme_contents[end_pos:]
        )

        # Write the updated contents back to the README file
        with open("README.md", "w") as file:
            file.write(updated_contents)
    else:
        print("Section not found in README.")

if __name__ == "__main__":
    main()
