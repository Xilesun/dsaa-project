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
    print('=== 毕业去向 ===')
    dream = statistics.calculate('dream')
    print(dream)
    print('=== 留学地点 ===')
    abroadCountry = statistics.calculate('abroadCountry')
    print(abroadCountry)
    print('=== 留学学校 ===')
    domesticUniversity = statistics.calculate('domesticUniversity')
    print(domesticUniversity)
    print('=== 预期月薪 ===')
    salary = statistics.calculate('salary')
    print(salary)

if __name__ == '__main__':
  run() 
