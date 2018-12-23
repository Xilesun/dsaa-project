# -*- coding: utf-8 -*-
import xlwt
import time
from itertools import chain, starmap
import numpy as np
import matplotlib.pyplot as plt;
import time
import matplotlib.font_manager as mfm

class Statistics:
  '''
  Parameters:
    students - a list of type Student
  '''
  def __init__(self, students):
    self.students = students
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

  '''
  Pluck the data of some fields
  Parameters:
    *fields (str,dict): the name of the fields to be pluck
  Output:
    [
      {field1: value},
      {field2: value},
      ...
    ]
  '''
  def pluck(self, *fields):
    result = []
    # Store into dict
    # result = [{field1: value, field2: value}, {...}, ...]
    row = {}
    for student in self.students:
      for field in fields:
        expects = []
        if isinstance(field, dict):
          expects = list(field.values())[0]
          field = list(field.keys())[0]
        value = getattr(student, field).strip()
        if expects and not value in expects:
          break
        row[field] = value
      if row:
        result.append(row.copy())
    return result   

  '''
  Summation, support multi-level
  Parameters:
    *fields (str,dict): the name of the fields to be pluck
  Output:
    [
      {
        field1: {
          data: ...,
          subfield1: { ... }
        }
      },
      {
        field2: ...
      },
      ...
    ]
  '''
  def calculate(self, *fields):
    result = {}
    data = self.pluck(*fields)
    for row in data:
      parent = result
      final = ''
      last_parent = {}
      for field in fields:
        if isinstance(field, dict):
          field = list(field.keys())[0]
        value = row[field]
        if value != '':
          # If there exists a process method, call it
          process = 'process{}'.format(field.capitalize())
          if hasattr(self, process) and callable(getattr(self, process)):
            value = getattr(self, process)(value)
          final = value
          last_parent = parent
          if value not in parent:
            parent[value] = {'data': 0}
          parent[value]['data'] += 1
          parent = parent[value]
        
    return result
    
  def processAbroadcountry(self, val):
    return val.replace('国', '')

  def processSalary(self, val):
    int_value = int(val)
    if  int_value > 1000:
      return str(int(int_value/1000))
    else :
      return val

  def compare(self, field1, field2):
    result = {}
    parent = {
      'Yes': {'data': 0}, 
      'No': {'data': 0}
    }
    data = self.pluck(field1, field2)
    for row in data:
      if row[field1]==row[field2]:
        parent['Yes']['data'] += 1
      else:
        parent['No']['data'] += 1
    result = parent
    return result
  
  def output(self, data, level=0):
    for k, v in data.items():
      if not isinstance(v, dict):
        pass
      else:
        print('{} - {} ({})'.format(' ' * level, k, v['data']))
        self.output(v, level + 1)
  
  def unpack(self, parent_key, parent_value):
    try:
      items = parent_value.items()
    except AttributeError:
      # parent_value was not a dict, no need to flatten
      yield (parent_key, parent_value)
    else:
      for key, value in items:
        if key != 'data':
          yield (parent_key + (key,), value)
        else:
          yield (parent_key, value)

  # Flatten the multilevel dict
  def flatten(self, dictionary):
    # Put each key into a tuple to initiate building a tuple of subkeys
    dictionary = {(key,): value for key, value in dictionary.items()}
    while True:
      # Keep unpacking the dictionary until all value's are not dictionary's
      dictionary = dict(chain.from_iterable(starmap(self.unpack, dictionary.items())))
      if not any(isinstance(value, dict) for value in dictionary.values()):
        break

    return dictionary  

  def exportToXls(self, data, title):
    wb = xlwt.Workbook('utf-8')
    ws = wb.add_sheet('data')
    n = len(data)
    keyList = list(data.keys())
    len2 = 0
    # Put the elements in tuple in the right place
    for x in range(n):
      tuple = keyList[x]
      len1 = len(tuple)
      ws.write(x, len1-1, tuple[len1-1])
      if len1 > len2:
        len2 = len1
    # Put the numbers of different keys in the right place
    for x in range(n):
      ws.write(x, len2, data[keyList[x]])
    t = time.time()
    name = './data/excel/{}-{}.xls'.format(title, str(int(t)))
    wb.save(name)
  
  '''
  Export data to a bar char
  Parameters:
    data (dict): a non-nested dict like {field: {data: value}, ...}
    title (str)
    yLable (str)
  '''
  def exportToBarchart(self, data, title='', yLabel=''):
    yData = ()
    xLabel = ()
    for k, v in data.items():
      xLabel += (u'{}'.format(k),)
      yData += (v['data'],)

    f = plt.figure(figsize=(15, 10))
    y_pos = np.arange(len(xLabel))
    ax = f.add_subplot(111)
    bars = ax.bar(y_pos, yData, align='center', width=0.5)
    ax.set_xticks(y_pos)
    ax.set_xticklabels(xLabel)
    ax.set_ylabel(u'{}'.format(yLabel))
    ax.set_title(u'{}'.format(title))

    for bar in bars:
      yval = bar.get_height()
      ax.text(bar.get_x(), yval + .01, yval)

    t = time.time()
    name = str(int(t))
    f.savefig('./data/graph/{}-{}.png'.format(title.replace(' ', ''), name))
  
  '''
  Export data to a pie char
  Parameters:
    data (dict): a non-nested dict like {field: {data: value}, ...}
    yLable (str)
  '''
  def exportToPiechart(self, data, title=''):
    pieData = ()
    labels = ()
    for k, v in data.items():
      labels += (u'{}'.format(k),)
      pieData += (v['data'],)

    f = plt.figure(figsize=(10, 10))
    ax = f.add_subplot(111)
    ax.pie(pieData, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    t = time.time()
    name = str(int(t))
    f.savefig('./data/graph/{}-{}.png'.format(title.replace(' ', ''), name))
