import sys
import re
import os
import urllib.parse # to URL encode a string

def replace_paths(html_path, subdir_name, new_subdir_name):
    '''
    Within the file at html_path, replace all
    instances of subdir_name with new_subdir_name.
    '''

    # Uses URL encoding to handle special characters (e.g. spaces are %20)
    old_name_encoded = urllib.parse.quote(subdir_name)
    new_name_encoded = urllib.parse.quote(new_subdir_name)

    # Update the file content
    with open(html_path, 'r') as f:
        content = f.read()
        content = re.sub(old_name_encoded, new_name_encoded, content)

    # Save the updated content
    with open(html_path, 'w') as f:
        f.write(content)

def replace_style(html_path, css_path):
    '''
    Within the file at html_path, replace the <style>...</style> block
    with a link to the css file at css_path.
    '''

    # This is how we attach a css file to an html file
    replace_str = f"<link rel=\"stylesheet\" type=\"text/css\" href=\"{css_path}\"/>"

    # The pattern to match the <style>...</style> block
    pattern = r"<style>.*?</style>"

    # Update the file content
    with open(html_path, 'r') as f:
        content = f.read()
        # Use re.DOTALL to make `.` match newline characters
        content = re.sub(pattern, replace_str, content, flags=re.DOTALL)

    # Save the updated content
    with open(html_path, 'w') as f:
        f.write(content)

def convert_dir(directory: str, css_path: str) -> list[tuple[str, str]]:
    '''
    This is a recursive function which will convert all subdirectories
    until it reaches the base case; no more subdirectories.

    @param directory: the directory to convert
    @param css_path: the path to the css file (relative to directory)

    @return: a list of tuples of the form (old_subdir_name, new_subdir_name)
    This is needed to update the html files of the parent directory as it
    references pages in the nested directories (if any).

    @explanation:
    The directory contains 0+ sub-directies (name is unknown) and one .html file (name is unknown).
    For the sake of explanation, let's assume the sub-directory is named 'assets' and that the .html file is named 'index.html'
    Repeat for the directory and every nested sub-directory:
    1. Chop off the ugly hex IDs at the end every html file / sub-directory
    3. Edit the HTML files to reflect the new names
    4. All all html files in a notion directory contain the same .css file. Replace all <style>...</style> blocks with a <link> tag that points to a single css file.
    '''

    print(f'CLEANING: {directory}')

    files: list[str] = os.listdir(directory)

    # We care about the html files (pages in the directory)
    html_filenames: list[str] = []
    for f in files:
        if f.endswith('.html'):
            html_filenames.append(f)

    if len(html_filenames) == 0:
        # BASE CASE: no pages in this directory
        return []
    else:
        # RECURSIVE CASE: directory has pages
        dir_replacements: list[tuple[str, str]] = []
        for html_name in html_filenames:

            # the subdir will have the same name as the html file (stores assets which includes subpages)
            subdir_name = html_name.removesuffix('.html')

            # Chop off ugly ID from file names:
            chop_idx = subdir_name.rfind(' ')
            chop_idx = min(chop_idx, len(subdir_name))  # this should not happen if you did not manually rename the folder
            new_subdir_name = subdir_name[:chop_idx]
            new_html_name = html_name[:chop_idx] + '.html'

            # Old paths
            html_path = os.path.join(directory, html_name)
            subdir_path = os.path.join(directory, subdir_name)

            # New paths
            new_html_path =     os.path.join(directory, new_html_name)
            new_subdir_path =   os.path.join(directory, new_subdir_name)

            # It's not guaranteed that the subdir exists (ie: no assets/subpages)
            hasSubpages = False

            # Html file will always exist, but check anyways:
            if os.path.isfile(html_path):
                replace_style(html_path, css_path)
                os.rename(html_path, new_html_path)
            if os.path.isdir(subdir_path):
                hasSubpages = True
                os.rename(subdir_path, new_subdir_path)

            # Reflect the rename within THIS DIRECTORY's html file:

            replace_paths(new_html_path, subdir_name, new_subdir_name)

            dir_replacements.append((subdir_name, new_subdir_name))

            if hasSubpages:
                # Recurse on each subdir
                subdir_replacements = convert_dir(new_subdir_path, css_path)
                for replace in subdir_replacements:
                    replace_paths(new_html_path, replace[0], replace[1])

        return dir_replacements


def main(dir, css_path, convert_multiple=False):
    # recursive function which will convert all subdirectories
    if not convert_multiple:
        convert_dir(dir, css_path)
    else:
        # => dir specifies a folder with multiple note folders (exports from Notion):
        # so repeat the process for each note folder:

        # get the list of all folders inside dir:
        subdirs = os.listdir(dir)
        subdirs = list(filter(lambda f: os.path.isdir(os.path.join(dir, f)), subdirs))
        directories = [os.path.join(dir, f) for f in subdirs]

        N = len(directories)
        for i, directory in enumerate(directories):
            print(f"NOTE {i+1}/{N}: {directory}")
            convert_dir(directory, css_path)


# call the main function with the directory from the command line
if __name__ == '__main__':
    '''
    Arguments:
    1. The directory to convert
    2. The path to the css file (relative to the directory)
    3. (optional) -m: wether or not to convert multiple directories or just one
    '''

    args = sys.argv[1:]
    dir, css_path = args[:2]

    convert_multiple = (len(args) == 3 and args[2] == '-m')

    main(dir, css_path, convert_multiple)