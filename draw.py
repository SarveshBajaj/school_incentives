#the draw

import numpy as np
import pickle as pkl
from student import Student,School
students = pkl.load(open("students.p", "rb"))
schools_load = pkl.load(open("schools.p", "rb"))

assignments = {}
schools = {}
for s in schools_load:
	schools[s.name] = s.capacity
	assignments[s.name] = set()

for student in students:
	for i in xrange(len(student.rankings)):
		student.rankings[i] = student.rankings[i].strip()
		if student.rankings[i] == "AlvaraoIMMS":
			student.rankings[i] = "AlvaradoIMMS"
		if student.rankings[i] == "King":
			student.rankings[i] = "Starr King"
		if student.rankings[i] == "KingIMMM":
			student.rankings[i] = "Starr KingIMMM"

def draw():
	lottery = np.random.permutation(len(students))
	it = 0
	for i in lottery:
		it +=1
		print it
		stud = students[i]

		cur_rank = 0
		while cur_rank < stud.private_schoool_cutoff:
			cur_school = stud.rankings[cur_rank]
			if schools[cur_school] > 0:
				assignments[cur_school].add(stud)
				schools[cur_school] -=1
			cur_rank +=1
	pkl.dump(assignments, open("draw_assignments.p", "wb"))

draw()
