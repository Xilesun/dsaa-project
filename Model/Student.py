# -*- coding: utf-8 -*-

class Student:
  '''
  Parameters:
    data - a dict contains the data of each student
  '''
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.sex = data['sex']
    self.province = data['province']
    self.city = data['city']
    self.district = data['district'] # 区县
    self.gaokao = data['gaokao'] # 高考成绩
    self.sustech = data['sustech'] # 能测成绩
    self.gpa = data['gpa']
    self.dream = data['dream'] # 毕业去向
    self.abroadCountry = data['abroadCountry']
    self.abroadUniversity = data['abroadUniversity']
    self.major1 = data['major1'] # 出国专业
    self.domesticCity = data['domesticCity']
    self.domesticUniversity = data['domesticUniversity']
    self.major2 = data['major2'] # 考研专业
    self.workProvince = data['workProvince']
    self.workCity = data['workCity']
    self.degree = data['degree']
    self.workPlace = data['workPlace']
    self.salary = data['salary'] # 单位: k
