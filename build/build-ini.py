import configparser
import datetime
import pathlib

def var_replace_page(page, html):
    if "{{ page.updated }}" in html:
        updated = pathlib.Path(page).stat().st_mtime
        updated = datetime.datetime.fromtimestamp(updated).strftime("%Y-%m-%d %H:%M:%S")
        html = html.replace("{{ page.updated }}", updated)
    return html

def main():
    print("Read config and blog ini files.")
    # Load the site config ini file
    config = configparser.ConfigParser()
    config.read("site.ini")

    # Load the blog config ini file
    blog = configparser.ConfigParser()
    blog.read("blog.ini")

    print("Store blog post data.")
    #posts = {}
    blog_categories = []


    #for blog_key, blog_value in blog["blog_posts"].items():
    #    posts[blog_key] = {}
    #    for post_key, post_value in blog[blog_key].items():
    #        posts[blog_key][post_key] = post_value

    for blog_key, blog_url in blog["blog_posts"].items():
        print(blog_key)
        for post_key, post_value in blog[blog_key]:
            blog_categories =
    #print(blog_categories)

    # Welcome message and menu
    print("\n-------------------------------------------------")
    print("              plind.us Site Builder")
    print("-------------------------------------------------\n")

    # ====================================================
    # Generate element files from template
    # ====================================================
    print("Generate element files from template:")

    # Loop through each element
    for element_key, element_value in config["elements"].items():
        print(" -> " + element_key + ": " + element_value)

        # Open the element html file and store the content
        with open("template/elements/" + element_value, "r") as element:
            html = element.read()

        # Loop through each site variable and replace with values
        for variable_key, variable_value in config["site"].items():
            html = html.replace("{{ var." + variable_key + " }}", variable_value)

        # Look through each blog variable and replace with values
        #if "{{ blog.link_category }}" in html:

        # Save the final text to the workspace html file
        with open("workspace/" + element_value, "w") as workspace:
            workspace.write(html)


    # ====================================================
    # Generate pages from template
    # ====================================================
    print("Generate pages from template:")

    # Loop through each page
    for page_key, page_value in config["pages"].items():
        print(" -> " + page_key + ": " + page_value)

        # Open the page html file and store the content
        with open("template/pages/" + page_value, "r") as page:
            page_html = page.read()

        # Loop through each variable and replace with values
        for variable_key, variable_value in config["site"].items():
            page_html = page_html.replace("{{ var." + variable_key + " }}", variable_value)

        # Loop through each element and include
        for element_key, element_value in config["elements"].items():
            if "{{ inc." + element_key + " }}" in page_html:
                with open("workspace/" + element_value, "r") as element:
                    element_html = element.read()
                page_html = page_html.replace("{{ inc." + element_key + " }}", element_html)

        # Loop through each page variable and replace with values
        page_html = var_replace_page("template/pages/" + page_value, page_html)

        # Save the final html file to the content directory
        with open("../www/" + page_value, "w") as content:
            content.write(page_html)


    # ====================================================
    # Generate blog posts from template
    # ====================================================
    print("Generate blog posts from template:")

    # Loop through each page
    for blog_key, blog_value in blog["blog_posts"].items():
        print(" -> " + blog_key + ": " + blog_value)

        # Open the blog html file and store the content
        with open("template/pages/" + blog_value, "r") as page:
            blog_html = page.read()

        # Loop through each variable and replace with values
        for variable_key, variable_value in config["site"].items():
            blog_html = blog_html.replace("{{ var." + variable_key + " }}", variable_value)

        # Loop through each element and include
        for element_key, element_value in config["elements"].items():
            if "{{ inc." + element_key + " }}" in blog_html:
                with open("workspace/" + element_value, "r") as element:
                    element_html = element.read()
                blog_html = blog_html.replace("{{ inc." + element_key + " }}", element_html)

        # Loop through each page variable and replace with values
        blog_html = var_replace_page("template/pages/" + blog_value, blog_html)

        # Save the final html file to the content directory
        with open("../www/" + blog_value, "w") as content:
            content.write(blog_html)

if __name__ == "__main__":
    main()
