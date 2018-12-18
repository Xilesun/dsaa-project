# encoding=utf-8

class Statistics:
  def __init__(self, students):
    self.students = students

  # 取出某字段的所有数据
  def pluck(self, field):
    result = []
    for student in self.students:
      result.append(getattr(student, field))
    return result

  def calculate(self, field):
    result = {}
    data = self.pluck(field)
    for i in data:
      if i == '':
        i = '未知'
      if i in result:
        result[i] += 1
      else:
        result[i] = 1
    return result
