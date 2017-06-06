
names = ['rafael', 'paula', 'durval']
dict = {}
lst = []
#dict = {key: value for (key, value) in iterable}

for name in names:
    dict["name"] = name
    lst.append(dict.copy())

print(lst)
