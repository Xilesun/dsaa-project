import click
import csv
from Model.Student import Student
from Model.Statistics import Statistics

@click.command()
@click.option('--file', default='data/ProjectData.csv')
def run(file):
  # The fields of students
  keys = [
    'id', 
    'name', 
    'sex', 
    'province', 
    'city', 
    'district',
    'gaokao',
    'sustech',
    'gpa',
    'dream',
    'abroadCountry',
    'abroadUniversity',
    'major1',
    'domesticCity',
    'domesticUniversity',
    'major2',
    'workProvince',
    'workCity',
    'degree',
    'workPlace',
    'salary'
  ]
  data = {}
  students = []
  with open(file, newline='', encoding ='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    count = 0
    print('=== Reading Data... ===')
    for row in csv_reader:
      # Skip the row of titles
      if count != 0:
        for i, key in enumerate(keys):
          data[key] = row[i]
        student = Student(data)
        students.append(student)
        print('ID: {}, Name: {}'.format(student.id, student.name))
      count += 1
    print('=== Read Process Finished, Total: {} students ==='.format(count))
    statistics = Statistics(students)
    print('=== 居住地 ===')
    location = statistics.calculate(
      'province',
      'city', 
      'district'
    )
    statistics.output(location)
    print('=== 毕业去向 ===')
    dream = statistics.calculate(
      'dream',
      'abroadCountry', 
      'abroadUniversity', 
      'major1',
      'domesticCity',
      'domesticUniversity',
      'major2',
    )
    # statistics.output(dream)
    # print('=== 国内外升学意愿 ===')
    # study = statistics.calculate(
    #   {'dream': ['出国留学', '香港读研', '内地读研']},
    #   'degree'
    # )
    # statistics.output(study)
    # print('=== 升学意愿单项对比 ===')
    # degree = statistics.calculate('degree')
    # statistics.output(degree)
    # print('=== 工作目标城市及工作类型 ===')
    # work = statistics.calculate(
    #   'workProvince',
    #   'workCity',
    #   'workPlace'
    # )
    # statistics.output(work)
    # print('=== 月薪 ===')
    # salary = statistics.calculate('salary')
    # statistics.output(salary)
    # print('=== 是否在家乡工作 ===')
    # athome = statistics.compare('workCity','city')
    # statistics.output(athome)
    print(statistics.flatten(dream))

if __name__ == '__main__':
  run() 
