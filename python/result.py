from bs4 import BeautifulSoup

def parse_result(page):
    table = BeautifulSoup(page, "html.parser")
    keys = ['course',
            'sessional_marks',
            'exam_marks',
            'total',
            'grace',
            'grades']


    credit_keys = ['facult_number', 'enrolment', 'name', 'ec', 'spi', 'cpi']
    dataset = dict()


    cred_table = table.find('table', {'style':'width:100%;text-align:center;'})
    for row in cred_table.find_all('tr')[1:]:
        dataset= dict(zip(credit_keys, (m.get_text()for m in row.find_all('td'))))
    
    dataset['result'] = list()
    res_table = table.find('table', {'class':"table table-hover"})
    
    for row in res_table.find_all('tr')[1:]:
        x = dict(zip(keys, (m.get_text() for m in row.find_all('td'))))
        dataset['result'].append(x)
    
    return dataset