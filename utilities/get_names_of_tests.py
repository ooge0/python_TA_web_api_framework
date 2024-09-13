import subprocess

from utilities.general_utils import GeneralUtils


def get_test_names(test_dir):
    result = subprocess.run(['pytest', '--collect-only', test_dir, '--no-header'], stdout=subprocess.PIPE,
                            text=True)
    output = result.stdout
    print(output)
    # Parse the output to extract tests names
    names = []
    for line in output.splitlines():
        if line.startswith('  <Function'):
            name = line.split('<Function ')[1].split('>')[0]
            names.append(name)
    return names


if __name__ == "__main__":
    utils = GeneralUtils()
    test_dir = "../tests/web_app_tests"  # Replace with your tests directory path
    file_path = "../resources/existing_tests_in_the_project.txt"  # Creates the file in a specific location
    test_list = get_test_names(test_dir)
    utils.create_file_and_write_test_names(test_list, file_path)
