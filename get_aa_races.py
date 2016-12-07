import pickle as pkl
from student import Student,School
from collections import Counter
students = pkl.load(open("students.p", "rb"))
#schools = pkl.load(open("schools.p", "rb"))


aa_racial_dist = {}

def white_and_asian(dist):
	return 1.0 * (dist["white"] + dist["asian"]) / sum(dist.values()) 

def black_and_latino(dist):
	return 1.0 * (dist["hisp"] + dist["black"]) / sum(dist.values()) 

def racially_isolated(dist):
	race, ct = dist.most_common(1)[0] 
	ct *= 1.0
	return ct / sum(dist.values()) >= 0.6

for student in students:
	if student.att_area not in aa_racial_dist:
		aa_racial_dist[student.att_area] = Counter()
	aa_racial_dist[student.att_area][student.race] += 1

isolated = 0
for school in aa_racial_dist:
	if racially_isolated(aa_racial_dist[school]):
		print school + " (isolated)"
		print aa_racial_dist[school]
		isolated += 1
	else:
		print school + " (not isolated)"
		print white_and_asian(aa_racial_dist[school])
		print black_and_latino(aa_racial_dist[school])
	print "----------------"

print isolated