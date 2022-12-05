import html

# This is the input HTML string that we want to parse
html_string = "<html><head><title>Hello, World!</title></head><body><h1>Hello, World!</h1></body></html>"

# Parse the HTML string into a DOM (Document Object Model) tree
dom_tree = html.fromstring(html_string)

# Extract the title element from the DOM tree
title_element = dom_tree.xpath('//title')[0]

# Extract the text inside the title element
title_text = title_element.text

# Print the title text
print(title_text)
