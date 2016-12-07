import pickle as pkl
from student import Student,School
students = pkl.load(open("students.p", "rb"))
schools = pkl.load(open("schools.p", "rb"))

#go through all schools
assignments = {}
assigned_students = {}
for school in schools:
	#look at all students CTIP1 who put school as first choice
	cap = school.capacity
	for student in students:
		if school.name in student.rankings[:student.private_schoool_cutoff]:
			if int(student.ct) == 1 and cap > 0:
				if student not in assignments:
					assignments[student] = []
				assignments[student].append(school)
				cap -=1
'''
for s in assignments:
	print '-----------------'
	print s.race, s.rankings[0]
	for sch in assignments[s]:
		print sch.name
	print '-----------------'
'''

for student in assignments:
	first_choice = student.rankings[0]
	for school in assignments[student]:
		if school.name.strip() == first_choice.strip():
			assigned_students[student] = school.name
			schools[school].capacity -=1

print len([student for student in students if int(student.ct) == 1])
print len(assigned_students)
				
