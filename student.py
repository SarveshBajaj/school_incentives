from random import random


class Student:
	def __init__(self):
		self.ct = None
		self.att_area = None
		self.rankings = None
		self.private_schoool_cutoff = None
		self.race = None

class School:
	def __init__(self,name,cap):
		self.name = name
		self.capacity = cap


# add points for immersion -- normal(30, 70)

# add for close -- normal(30, 70)

# p(ranking next) = score / (total score left)



