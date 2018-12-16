import click
import csv
from Student import Student

@click.command()
@click.option('--file', default='data/Project_data_20181208.csv')
def run(file):
  with open(file, newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
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
      for i, key in enumerate(keys):
        data[key] = row[i]
      student = Student(data)
      print(student.__dict__)

if __name__ == '__main__':
  run() 
