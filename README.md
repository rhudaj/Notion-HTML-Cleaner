# Notion-HTML-Cleaner

## About The Project

The purpose of this project is to automate the process of cleaning and restructuring HTML files and their associated directories. This includes renaming files and directories by removing redundant identifiers, replacing inline `<style>` tags with linked CSS files, and updating all internal references to reflect the changes.

The project provides a Python script that recursively processes HTML directories, ensuring all subdirectories and nested HTML files are handled seamlessly.

### Built With

* [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](#)
* [![Regex](https://img.shields.io/badge/Regex-%23E34F26.svg)](#)


## Usage

This script is designed to streamline managing large HTML directories. Use it to:

1. Replace `<style>` tags in HTML files with `<link>` tags that point to a single external CSS file.
2. Rename files and directories to cleaner versions by removing unnecessary identifiers (e.g., hex IDs).
3. Update references within HTML files to ensure consistency after renaming files and directories.

To run the script:

```bash
python cleaner.py <directory_path> <css_file_path>
```

- `directory_path`: The root directory containing HTML files and subdirectories.
- `css_file_path`: The relative or absolute path to the CSS file that will be linked to the HTML files.

Example:

```bash
python script.py ./notion_files ./styles/main.css
```

<!-- CODE STRUCTURE -->
## Code Structure

`replace_paths(html_path, subdir_name, new_subdir_name)`

- Replaces all occurrences of `subdir_name` with `new_subdir_name` in the provided HTML file.

`replace_style(html_path, css_path)`

- Replaces inline `<style>` blocks in the provided HTML file with a `<link>` tag to the given CSS file.

`convert_dir(directory: str, css_path: str)`

- Recursively processes a directory and its subdirectories, performing renames and replacements.

`main(dir, css_path)`

- Entry point that initiates the conversion process for a given directory.

## Getting Started

### Prerequisites

* Python 3.8 or newer installed

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/rhudaj/HTML-Cleaner.git
   ```
2. Navigate to the directory
   ```sh
   cd HTML-Cleaner
   ```

3. Add your Notion HTML exported folder.
    - For example ```./my_note```

4. Add your CSS file.

    - The CSS file that notion uses is already included: ```./notion_styles.css```, so you can use that or add your own

5. Run the script:

    - ```python cleaner.py ./my_note ./notion_styles.css```



## Roadmap

- [ ] Expand CSS customization options.
- [ ] Optimize performance for directories with thousands of files.


## Contact

Roman Hudaj - rhudaj@uwaterloo.ca
Project Link: [HTML Cleaner](https://github.com/rhudaj/HTML-Cleaner)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
