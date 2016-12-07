import pickle as pkl
from student import Student,School
from collections import Counter
students = pkl.load(open("students.p", "rb"))
schools = pkl.load(open("schools.p", "rb"))

assignments = pkl.load(open("assignments10percent.p", "rb"))
assignments_flipped = pkl.load(open("assignments10-flipped.p", "rb"))

isolated_schools = {}


def racially_isolated(race_ctr):
	total = 1.0 * sum([race_ctr[race] for race in race_ctr])
	for race in race_ctr:
		if race_ctr[race] / total > 0.6:
			return race

	return None


capacities = {}
for school in schools:
	school.capacity /= 10.0
 	school.capacity = int(round(school.capacity))
	capacities[school.name] = school.capacity

for school in assignments:
	print "------"
	print school
	print capacities[school]
	print len(assignments[school])
	print len(assignments_flipped[school])
	racial_dist = Counter([student.race for student in assignments[school]])
	print str(racially_isolated(racial_dist))
	racial_dist = Counter([student.race for student in assignments[school]])
	print str(racially_isolated(racial_dist))
