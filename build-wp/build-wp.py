import csv
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
# wp_posts csv row index:
# 0  ID                     {post:id}
# 1  post_author
# 2  post_date              {post:post_year},{post:post_month},{post:post_day},
#                           {post:post_date_full}
# 3  post_date_gmt
# 4  post_content           {post:post_content}
# 5  post_title             {post:post_title}
# 6  post_excerpt
# 7  post_status
# 8  comment_status
# 9  ping_status
# 10 post_password
# 11 post_name              {post:post_name}
# 12 to_ping
# 13 pinged
# 14 post_modified
# 15 post_modified_gmt
# 16 post_content_filtered
# 17 post_parent
# 18 guid
# 19 menu_order
# 20 post_type
# 21 post_mime_type
# 22 comment_count

def main():
    post_csv = "wp_posts.csv"

    # with open(post_csv_file, newline='') as csvfile:
    #     post_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in post_csv:
    #         if row[17] == "0" and row[20] == "post":
    #             print("Post: " + row[0] + " - " + row[5])
    #             print("Looking for revisions...")
    #             for subrow in post_csv:
    #                 if subrow[7] == "inherit" and subrow[17] == row[0] and subrow[20] == "revision":
    #                     print("  Revision ID: " + subrow[0] + "\n  Post Date: " + subrow[2] + "\n  Post Title: " + subrow[5])

    with open(post_csv, "r") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        posts = [row for row in reader]
        
    for parent_post in posts:
        if parent_post['post_parent'] == "0" and parent_post['post_type'] == "post":
            print(f"Post: {parent_post['post_title']} (ID {parent_post['ID']}) created {parent_post['post_date']}")
                
            for sub_post in posts:
                if sub_post['post_status'] == "inherit" and sub_post['post_parent'] == parent_post['ID'] and sub_post['post_type'] == "revision":
                    print(f" * Sub Post: {sub_post['post_title']} (ID {sub_post['ID']}) saved {sub_post['post_date']}")


# =============================================================================
# Run Main
#
if __name__ == "__main__":
    main()
