import os
import re
import subprocess
from collections import defaultdict
from itertools import chain


def get_pytest_names(file_path, project_root):
    """Run pytest --collect-only to get the test names and locations."""
    try:
        # Run pytest with --collect-only to list test details
        result = subprocess.run(['pytest', '--collect-only', '-q', file_path], capture_output=True, text=True,
                                cwd=project_root, check=False)  # check=False to avoid stopping on errors
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error running pytest: {e}")
        return None, None


def extract_test_info(pytest_output):
    """Extract test names and file paths with line numbers from pytest output."""
    test_info = []
    for line in pytest_output.splitlines():
        # Matching patterns like tests/test_sample.py::test_example
        match = re.search(r'(\S+\.py)::(\S+)', line)
        if match:
            file_path, test_name = match.groups()
            # Append the test file and name to the list
            test_info.append((file_path, test_name))
    return test_info


def escape_md_special_chars(text):
    """Escape special Markdown characters such as square brackets and ampersands."""
    # Escape square brackets and ampersands by adding a backslash before them
    return text.replace('[', r'\[').replace(']', r'\]').replace('&', r'\&')


def escape_md_special_chars(text):
    """Escape special Markdown characters such as square brackets and ampersands."""
    return text.replace('[', r'\[').replace(']', r'\]').replace('&', r'\&')


def generate_md_links(test_info, base_dir):
    """Generate a dictionary of markdown links grouped by test class (if '::' is present)."""
    md_links = defaultdict(list)  # Using defaultdict to group test names under their class/category

    for file_path, test_name in test_info:
        abs_file_path = os.path.abspath(file_path)
        relative_path = os.path.relpath(abs_file_path, base_dir)

        # Escape special characters in the test name for Markdown
        escaped_test_name = escape_md_special_chars(test_name)

        # Split the test_name by '::' to separate the category (class) and method
        if "::" in escaped_test_name:
            category, method = escaped_test_name.split("::", 1)
        else:
            category, method = "Miscellaneous", escaped_test_name  # Group tests without '::' under "Miscellaneous"

        # Create the markdown link for the method
        md_link = f"[{method}]({relative_path})"

        # Append the link under the respective category
        md_links[category].append(md_link)

    return md_links


def write_md_file(md_links, output_file):
    """Write the markdown links to an output file, grouped by category."""
    # total_tests = len(list(chain.from_iterable(md_links.values())))  # Flatten and count total tests
    # total_tests = sum(len(links) for links in md_links.values())  # Count total tests
    total_tests = sum([len(links) for links in md_links.values()])  # List comprehension for counting

    with open(output_file, 'w') as f:
        f.write(f"\n ### Test List\nTotal tests: {total_tests}\n")
        # Iterate over each category and its associated links
        category_count = 1
        for category, links in md_links.items():
            f.write(f"#### {category_count}. {category}\n")
            link_count = 1
            for link in links:
                f.write(f"{link_count}. {link}\n")
                link_count += link_count
            f.write(f"\n")
            category_count += 1


def main(test_file_path, output_md_file):
    """Main function to get test names and generate markdown file."""
    # Get the project root directory (one level up from the current directory)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("project_root:", project_root)
    pytest_output, pytest_error = get_pytest_names(test_file_path, project_root)

    if pytest_error:
        print(f"Warning: Some errors occurred during test collection:\n{pytest_error}")

    if not pytest_output:
        print("No tests found or error occurred.")
        return

    test_info = extract_test_info(pytest_output)
    if not test_info:
        print("No test information could be extracted.")
        return

    md_links = generate_md_links(test_info, project_root)
    write_md_file(md_links, output_md_file)
    print(f"Markdown file generated at: {output_md_file}")


if __name__ == "__main__":
    data = {
        2: {"test_file_path": "../",
            "output_md_file": "ta_framework_ui_api/resources/md_file_tests_output.md"},
    }
    main(**data[2])