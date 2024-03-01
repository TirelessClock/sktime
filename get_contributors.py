import requests

def get_contributors(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    response = requests.get(url)
    contributors = response.json()
    return contributors

def update_readme(owner, repo, contributors):
    # Define the HTML template for the widget
    widget_template = (
        '<a href="{profile_url}">'
        '<img src="{avatar_url}" alt="{username}" title="{username}" width="50" height="50">'
        '</a>'
    )

    # Generate HTML widgets for each contributor
    widgets = [widget_template.format(
        profile_url=contributor['html_url'],
        avatar_url=contributor['avatar_url'],
        username=contributor['login']
    ) for contributor in contributors]

    # Combine widgets into a single HTML string
    widgets_html = '\n'.join(widgets)

    # Read existing contents of the README file
    with open("README.md", "r") as file:
        readme_contents = file.read()

    # Define the start and end markers for the section to update
    start_marker = "<!--START_CONTRIBUTORS_WIDGET-->"
    end_marker = "<!--END_CONTRIBUTORS_WIDGET-->"

    # Find the start and end positions of the section to update
    start_pos = readme_contents.find(start_marker)
    end_pos = readme_contents.find(end_marker, start_pos + len(start_marker))

    # If the section exists, replace it with the updated information
    if start_pos != -1 and end_pos != -1:
        updated_section = f"{start_marker}\n{widgets_html}\n{end_marker}"
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
    owner = "TirelessClock"
    repo = "sktime"
    contributors = get_contributors(owner, repo)
    contributors = contributors[:5]
    update_readme(owner, repo, contributors)