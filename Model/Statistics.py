# encoding=utf-8
import xlwt

class Statistics:
  def __init__(self, students):
    self.students = students

  # Pluck the data of some fields
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

  # 统计数字，支持多层级
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
  
  def output(self, data, level=0):
    for k, v in data.items():
      if not isinstance(v, dict):
        pass
      else:
        print('{} - {} ({})'.format(' ' * level, k, v['data']))
        self.output(v, level + 1)
  
  # def exportToXls(self, data):
  #   wb = xlwt.Workbook()
  #   ws = wb.add_sheet('data')
  #   level = 0
  #   while isinstance(data, dict):
  #   for  k, v) in enumerate(data.items()):
  #       ws.write(index, level, v['data'])
  #     level += 1
  #     data = 

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
    parent = {'Yes':{'data':0},'No':{'data':0}}
    data = self.pluck(field1, field2)
    for row in data:
      if row[field1]==row[field2]:
        parent['Yes']['data'] += 1
      else:
        parent['No']['data'] += 1
    result = parent
    return result