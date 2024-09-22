import os
import re
import subprocess
from collections import defaultdict


def get_pytest_names(file_path, project_root):
    """Run pytest --collect-only to get the test names and locations."""
    try:
        # Convert relative file path to absolute path
        abs_file_path = os.path.abspath(file_path)
        result = subprocess.run(['pytest', '--collect-only', '-q', abs_file_path], capture_output=True, text=True,
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
    """Escape special MarkDown characters such as square brackets and ampersands."""
    return text.replace('[', r'\[').replace(']', r'\]').replace('&', r'\&')


def generate_md_links(test_info, base_dir) -> defaultdict(list):
    """Generate a dictionary of MarkDown links grouped by test class (if '::' is present)."""
    md_links = defaultdict(list)  # Using defaultdict to group test names under their class/category

    for file_path, test_name in test_info:
        abs_file_path = os.path.abspath(file_path)
        relative_path = f"../{file_path.split('python_TA_web_api_framework/')[1]}"

        # Escape special characters in the test name for MarkDown
        escaped_test_name = escape_md_special_chars(test_name)

        # Split the test_name by '::' to separate the category (class) and method
        if "::" in escaped_test_name:
            category, method = escaped_test_name.split("::", 1)
        else:
            category, method = "Miscellaneous", escaped_test_name  # Group tests without '::' under "Miscellaneous"
        # Create the MarkDown link for the method
        md_link = f"[{method}]({relative_path})"

        # Append the link under the respective category
        md_links[category].append(md_link)

    return md_links


def write_md_file(md_links, output_file):
    """Write the MarkDown links to an output file, grouped by category."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    total_tests = sum(len(links) for links in md_links.values())  # List comprehension for counting

    with open(output_file, 'w') as f:
        f.write(f"\n ### Test List\nTotal tests: {total_tests}\n")
        # Iterate over each category and its associated links
        category_count = 1
        for category, links in md_links.items():
            f.write(f"#### {category_count}. {category}\n")
            link_count = 1
            for link in links:
                f.write(f"{link_count}. {link}\n")
                link_count += 1
            f.write(f"\n")
            category_count += 1


def main(test_file_path, output_md_file):
    """Main function to get test names and generate MarkDown file."""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("script_dir:", script_dir)

    # Compute absolute paths
    abs_test_file_path = os.path.abspath(os.path.join(script_dir, test_file_path))
    abs_output_md_file = os.path.abspath(os.path.join(script_dir, output_md_file))

    # Get the project root directory (one level up from the script's directory)
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

    pytest_output, pytest_error = get_pytest_names(abs_test_file_path, project_root)

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
    write_md_file(md_links, abs_output_md_file)


if __name__ == "__main__":
    data = {
        1: {"test_file_path": "../",
            "output_md_file": "../resources/list_of_all_project_tests.md"}
    }
    main(**data[1])
