from jinja2 import Template

name = 'Bill'
age = 28

tm = Template("My name is {{ name }} and I am {{ age }}")
msg = tm.render(name=name, age=age)

print(msg)# My name is Bill and I am 28

from jinja2 import Template

persons = [
    {'name': 'Andrej', 'age': 34},
    {'name': 'Mark', 'age': 17},
    {'name': 'Thomas', 'age': 44},
    {'name': 'Lucy', 'age': 14},
    {'name': 'Robert', 'age': 23},
    {'name': 'Dragomir', 'age': 54}
]

rows_tmp = Template("""{% for person in persons -%}
    {{ person.name }} {{ person.age }}
{% endfor %}""")

print(rows_tmp.render(persons=persons))

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('.'))

template = env.get_template("persons.html")

persons = [
    {'name': 'Andrej', 'age': 34},
    {'name': 'Mark', 'age': 17},
    {'name': 'Thomas', 'age': 44},
    {'name': 'Lucy', 'age': 14},
    {'name': 'Robert', 'age': 23},
    {'name': 'Dragomir', 'age': 54}
]

output = template.render(persons=persons, )

with open("new_persons.html", "w", encoding='utf-8') as fh:
    fh.write(output)
