import yaml
import datetime
import pathlib

def open_html(path):
    with open(path, "r") as file:
        html = file.read()
    return html

def write_html(path, html):
    with open(path, "w") as file:
        file.write(html)

def inc_element(config, html):
    for inc_key, inc_value in config:
        if "{{ inc." + inc_key + " }}" in html:
            inc_html = open_html("workspace/" + inc_value)
            html = html.replace("{{ inc." + inc_key + " }}", inc_html)
    return html

#def inc_blog(config, html):
#    if "{{ inc.blog_nav_category }}" in html:
#        html = html.replace("{{ inc.blog_nav_category }}", gen_blog_nav(config, "category"))
#    return html

def var_replace_site(config, html):
    for var_key, var_value in config:
        html = html.replace("{{ var." + var_key + " }}", var_value)
    return html

def var_replace_blog(config, html):
    for var_key in config:
        html = html.replace("{{ blog." + var_key + " }}", str(config[var_key]))
    return html

def var_replace_page(page, html):
    if "{{ page.updated }}" in html:
        updated = pathlib.Path(page).stat().st_mtime
        updated = datetime.datetime.fromtimestamp(updated).strftime("%Y-%m-%d %H:%M:%S")
        html = html.replace("{{ page.updated }}", updated)
    return html

#def gen_blog_nav(config, type):
    #nav = []
    #html = ""
    #
    #for var_key, var_value in config:
    #    nav.append(var_value[type])
    #
    #if type == "date":
    #elif type == "category":
    #    for category in set(sorted(nav)):
    #        html = html + "<li><a href=\"asd\">" + category + " <em>(" + str(nav.count(category)) + ")</em></a></li>\n"
    #return html

def main():
    print("\n-------------------------------------------------")
    print("              plind.us Site Builder")
    print("-------------------------------------------------\n")

    # Load the site config yaml
    print("Load site config yaml file... ", end = "")
    config = yaml.safe_load(open("site.yaml", "r"))
    print("done.")

    # Generate element files from template
    print("Generate common element files from template... ", end = "")
    for element_key, element_value in config["elements"].items():
        element_html = open_html("template/elements/" + element_value)
        element_html = var_replace_site(config["site"].items(), element_html)
        #element_html = inc_blog(config["blog_posts"].items(), element_html)
        write_html("workspace/" + element_value, element_html)
    print("done.")

    # Generate pages from template
    print("Generate complete web page files from template... ", end = "")
    for page_key, page_value in config["pages"].items():
        page_html = open_html("template/pages/" + page_value)
        page_html = var_replace_site(config["site"].items(), page_html)
        page_html = inc_element(config["elements"].items(), page_html)
        page_html = var_replace_page("template/pages/" + page_value, page_html)
        write_html("../www/" + page_value, page_html)
    print("done.")

    # Generate blog posts from template
    print("Generate complete blog posts from template... ", end = "")
    for blog_key, blog_value in config["blog_posts"].items():
        blog_html = open_html("template/pages/" + blog_value["url"])
        blog_html = var_replace_site(config["site"].items(), blog_html)
        blog_html = var_replace_blog(blog_value, blog_html)
        blog_html = inc_element(config["elements"].items(), blog_html)
        blog_html = var_replace_page("template/pages/" + blog_value["url"], blog_html)
        write_html("../www/" + blog_value["url"], blog_html)
    print("done.")

if __name__ == "__main__":
    main()
