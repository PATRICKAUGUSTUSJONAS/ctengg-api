from bs4 import BeautifulSoup
import json

def parse(doc):
    table = BeautifulSoup(doc, "html.parser")

    keys = ['course',
            'total',
            'attended',
            'percentage',
            'remark',
            'date']

    datasets = dict()
    datasets['attendance'] = list()

    datasets['name'] = table.find('strong').get_text().title()

    for row in table.find_all("tr")[1:]:
        dataset = dict(zip(keys, (td.get_text() for td in row.find_all("td"))))
        datasets['attendance'].append(dataset)

    return datasets