from bs4 import BeautifulSoup
import urllib
import json

page = """
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    <div class="table-responsive">
        <table class="table table-hover">
            <tr>
                <th>Course</th>
                <th>Sessional Marks</th>
                <th>Exam Marks</th>
                <th>Total</th>
                <th>Grace Marks</th>
                <th>Grades</th>
                <th>Grade Range</th>
            </tr>
            <tr>
                <td>AM261</td>
                <td>38</td>
                <td>49</td>
                <td>87</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
            <tr>
                <td>CO203</td>
                <td>34</td>
                <td>50</td>
                <td>84</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
            <tr>
                <td>CO206</td>
                <td>36</td>
                <td>56</td>
                <td>92</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
            <tr>
                <td>CO207</td>
                <td>37</td>
                <td>46</td>
                <td>83</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
            <tr>
                <td>CO291</td>
                <td>56</td>
                <td>35</td>
                <td>91</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
            <tr>
                <td>EL211</td>
                <td>29</td>
                <td>53</td>
                <td>82</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
            <tr>
                <td>EZ291</td>
                <td>53</td>
                <td>32</td>
                <td>85</td>
                <td>0</td>
                <td>A</td>
                <td>A: 75, B:60, C: 45 , D: 35</td>
            </tr>
        </table>
        <table style="width:100%;text-align:center;">
            <tr>
                <th style="text-align:center;">Faculty No.</th>
                <th style="text-align:center;">Enrol No.</th>
                <th style="text-align:center;">Student Name</th>
                <th style="text-align:center;">EC</th>
                <th style="text-align:center;">SPI</th>
                <th style="text-align:center;">CPI</th>
                <th style="text-align:center;">Result</th>
            </tr>
            <tr>
                <td>14PEB049</td>
                <td>GF1032</td>
                <td>AREEB JAMAL</td>
                <td>70</td>
                <td>10</td>
                <td>9.714</td>
                <td>CONTINUED</td>
            </tr>
        </table>
    </div>
    <center>
        <a href="cpiconvert.php" target="_blank">Click here to check your
        equivalent percentage...</a>
    </center>
</body>
</html>
"""

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