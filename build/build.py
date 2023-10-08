import yaml
import glob
import datetime
import pathlib
import re
import sys
import shutil


# =============================================================================
# List Files Function
#
# Purpose:
#   Create a list of all matching files in a specific directory (recursive).
#
# Parameters:
#   path           String     Required    Directory to search for files.
#
# Returns:
#   files          List                   Listing of all files found.
#
def list_files(path):
    if path == "pages" or path == "includes":
        search_path = "template/" + path + "/**/*.htm*"
    elif path == "static":
        search_path = "template/static/**/*.*"

    files = glob.glob(search_path, recursive=True)
    return files


# =============================================================================
# Open File Function
#
# Purpose:
#   Opens the specified file and store its contents.
#
# Parameters:
#   path           String     Required    Path of the file to open.
#
# Returns:
#   html           String                 Contents of the file.
#
def open_file(path):
    with open(path, "r") as file:
        html = file.read()
    return html


# =============================================================================
# Write File Function
#
# Purpose:
#   Write the variable contents to the specified file.
#
# Parameters:
#   path           String     Required    Path of the file to write.
#   html           String     Required    Complete contents of the file.
#
def write_file(path, html):
    with open(path, "w") as file:
        file.write(html)    


# =============================================================================
# Add Include Files Function
#
# Purpose:
#   Search the provided HTML for include placeholders (e.g. {inc:header.html}) 
#   and replace with content from the include file.
#
# Parameters:
#   html           String     Required    HTML content to search and update.
#
# Returns:
#   html           String                 Contents of the file.
#
def add_include_files(html):
    paths = list_files("includes")
    for path in paths:
        if "{inc:" + path.split("/")[-1] + "}" in html:
            include = open_file(path)
            html = html.replace("{inc:" + path.split("/")[-1] + "}", include)
    return html


# =============================================================================
# Add Dynamic Variables Function
#
# Purpose:
#   Search the provided HTML for variable placeholders (e.g. {var:updated}) 
#   and replace with current values.
#
# Parameters:
#   html           String     Required    HTML content to search and update.
#
# Returns:
#   html           String                 Contents of the file.
#
def add_dynamic_vars(html):
    if "{var:updated}" in html:
        updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = html.replace("{var:updated}", updated)
    return html


# =============================================================================
# Add Metadata Variables Function
#
# Purpose:
#   Search the provided HTML for metadata placeholders (e.g. {meta:title=abc}) 
#   and replace with specified values.
#
# Parameters:
#   html           String     Required    HTML content to search and update.
#
# Returns:
#   html           String                 Contents of the file.
#
def add_meta_vars(html):
    keys = re.findall(r"(?<=meta:).*(?=\=)", html)
    for key in keys:
        val_pos = re.search(r"(?<=meta:" + key + "=).*(?=})", html)
        html = html.replace("{meta:" + key + "}", html[val_pos.start():val_pos.end()])
        html = html.replace("{meta:" + key + "=" + html[val_pos.start():val_pos.end()] + "}", "")    
    return html


# =============================================================================
# Add Config Variables Function
#
# Purpose:
#   Search the provided HTML for config placeholders (e.g. {cfg:site_name}) 
#   and replace with values set in cfg.yaml.
#
# Parameters:
#   html           String     Required    HTML content to search and update.
#   config         Dict       Required    Config variables set in cfg.yaml.
#
# Returns:
#   html           String                 Contents of the file.
#
def add_config_vars(html, config):
    for key, value in config.items():
        html = html.replace("{cfg:" + key + "}", value)
    return html


# =============================================================================
# Cleanup Output
#
# Purpose:
#   Cleanup the output by removing empty lines.
#
# Parameters:
#   html           String     Required    HTML content to search and update.
#
# Returns:
#   html           String                 Contents of the file.
#
def cleanup(html):
    result = ""
    for line in html.splitlines():
        if line:
            result += line + "\n"
    return result


# =============================================================================
# Main Function
#
def main():
    config_file = "cfg.yaml"

    print("\n-------------------------------------------------")
    print("              plind.us Site Builder")
    print("-------------------------------------------------\n")

    #
    # Load the site config yaml
    #
    print(f"Load site config file {config_file}... ", end = "")

    try:
        config = yaml.safe_load(open(config_file, "r"))
    except FileNotFoundError as err:
        print(f"error!  {config_file} was not found.\n\n{err=}, {type(err)=}")
        sys.exit(1)
    except Exception as err:
        print(f"error!  {config_file} could not be loaded.\n\n{err=}, {type(err)=}")
        sys.exit(1)
    else:
        print("done.")

    #
    # Move static files
    #
    print("Copy static files... ", end = "")
    try:
        shutil.rmtree("build")
        shutil.copytree("template/static", "build")
    except Exception as err:
        print(f"error!  Static files could not be copied.\n\n{err=}, {type(err)=}")
        sys.exit(1)
    else:
        print("done.")

    #
    # Generate complete HTML files for each page in the template
    #
    print("Generate site pages... ")
    paths = list_files("pages")
    count = 0
    for path in paths:
        count += 1
        print(f"  ({count}/{len(paths)}) {path}  -->  ", end = "")
        try:
            html = open_file(path)
            html = add_include_files(html)
            html = add_dynamic_vars(html)
            html = add_meta_vars(html)
            html = add_config_vars(html, config)
            html = cleanup(html)
            write_file(path.replace("template/pages", "build"), html)
        except Exception as err:
            print(f"error!  {path} could not be generated.\n\n{err=}, {type(err)=}")
            sys.exit(1)
        else:
            print(f"{path.replace('template/pages', 'build')}")


# =============================================================================
# Run Main
#
if __name__ == "__main__":
    main()
