from jinja2 import Environment, FileSystemLoader

# Create a Jinja2 environment with the loader pointing to the correct directory
env = Environment(loader=FileSystemLoader('C:/Project/myProject/modul_4_socket_server/app/templates'))

# Now Jinja2 can find the 'persons.html' template
template = env.get_template("persons.html")

persons = [
    {'name': 'Andrej', 'age': 34},
    {'name': 'Mark', 'age': 17},
    {'name': 'Thomas', 'age': 44},
    {'name': 'Lucy', 'age': 14},
    {'name': 'Robert', 'age': 23},
    {'name': 'Dragomir', 'age': 54}
]

# Render the template
output = template.render(persons=persons)

# Write the rendered output to a new HTML file
with open("new_persons.html", "w", encoding='utf-8') as fh:
    fh.write(output)