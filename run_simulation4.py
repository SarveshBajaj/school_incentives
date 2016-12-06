import random
import copy
import pickle as pkl
from student import Student,School
students = pkl.load(open("students.p", "rb"))
schools = pkl.load(open("schools.p", "rb"))

students = random.sample(students, int(round(len(students) / 10.0)))

for school in schools:
	school.capacity /= 10.0
	school.capacity = int(round(school.capacity))

# fix student school names
for student in students:
	for i in xrange(len(student.rankings)):
		student.rankings[i] = student.rankings[i].strip()
		if student.rankings[i] == "AlvaraoIMMS":
			student.rankings[i] = "AlvaradoIMMS"
		if student.rankings[i] == "King":
			student.rankings[i] = "Starr King"
		if student.rankings[i] == "KingIMMM":
			student.rankings[i] = "Starr KingIMMM"

# A = School("A",  1)
# B = School("B", 1)
# C = School("C", 1)

# one = Student()
# one.rankings = ["A","B","C"]
# one.ct = 2
# one.att_area = "B"

# two = Student()
# two.rankings = ["C","B","A"]
# two.ct = 2
# two.att_area = "C"

# three = Student()
# three.rankings = ["B","C","A"]
# three.ct = 2
# three.att_area = "A"


# schools = [A, B, C]
# students = [one, two, three]

#students = students[1:200]
num_assigned = 0
num_students = len(students)
tent_offers = {} # map from school name to students
tent_offers_student = {}
assignments = {} # map from school name to students
assigned_students = set() # students who have accepted an offer
capacities = {} # school name --> capacity
full_schools = set()



# initialization
for school in schools:
	tent_offers[school.name] = []
	assignments[school.name] = []
	capacities[school.name] = school.capacity

for student in students:
	tent_offers_student[student] = set()

def make_offers():
	new_cap = 0
	for school in schools:
		if (len(tent_offers[school.name]) + len(assignments[school.name])) < school.capacity:
			new_cap += school.capacity - len(tent_offers[school.name]) - len(assignments[school.name])
			ctip = []
			aa = []
			other = []
			for student in students:
				if student not in assigned_students:
					if school.name in student.rankings:
						if int(student.ct) == 1:
							ctip.append(student)
						elif student.att_area == school.name:
							aa.append(student)
						else:
							other.append(student)
			random.shuffle(ctip)
			random.shuffle(aa)
			random.shuffle(other)
			offers = []
			cap_remaining = school.capacity - len(tent_offers[school.name]) - len(assignments[school.name])
			offers.extend(ctip[0:cap_remaining])
			if len(offers) < cap_remaining:
				offers.extend(aa[0:(cap_remaining - len(offers))])
			if len(offers) < cap_remaining:
				offers.extend(other[0:(cap_remaining - len(offers))])
			tent_offers[school.name].extend(offers)
			for offer in offers:
				tent_offers_student[offer].add(school.name)
	print "new capacity = " + str(new_cap)
	return new_cap

def accept_offers():
	offers_removed = 0
	for student in students:
		if student not in assigned_students:
			first_empty = -1
			for i in xrange(len(student.rankings)):
				if student.rankings[i] not in full_schools:
					first_empty = i
					break
			if first_empty >= 0:
				school = student.rankings[first_empty]
				school_offers = tent_offers[school]
				if student in school_offers:
					assignments[school].append(student)
					assigned_students.add(student)
					#num_assigned += 1
					offers = tent_offers_student[student]
					offers_removed += len(offers) -1
					for sch in offers:
						tent_offers[sch].remove(student)
					tent_offers_student[student] = [sch for sch in tent_offers_student[student] if sch == school]
					if len(assignments[school]) == capacities[school]:
						 full_schools.add(school)
	return offers_removed

def is_cycle(backtrack, student, school):
	cur_school, cur_student = school, student
	prev_school, prev_student = backtrack[(school, student)]
	while((prev_school, prev_student) != (school, student)):
		cur_school = prev_school
		cur_student = prev_student
		if backtrack[(cur_school, cur_student)] is None:
			return False
		prev_school, prev_student = backtrack[(cur_school, cur_student)]
	return True

def trade_cycle(backtrack, student, school):
	if not is_cycle(backtrack, student, school):
		return False
	#print student
	#print school
	cur_school, cur_student = school, student
	prev_school, prev_student = backtrack[(school, student)]
	while((prev_school, prev_student) != (school, student)):
		tent_offers[cur_school].remove(cur_student)
		tent_offers[cur_school].append(prev_student)

		tent_offers_student[cur_student].remove(cur_school)
		tent_offers_student[prev_student].add(cur_school)

		cur_school = prev_school
		cur_student = prev_student
		if backtrack[(cur_school, cur_student)] is None:
			print cur_school
			print backtrack
			print []
		prev_school, prev_student = backtrack[(cur_school, cur_student)]

	tent_offers[cur_school].remove(cur_student)
	tent_offers[cur_school].append(prev_student)

	tent_offers_student[cur_student].remove(cur_school)
	tent_offers_student[prev_student].add(cur_school)	
	return True

def make_pref_graph():
	graph = {} # (school, student) --> (school, student) where student has offer at school which is better than current best offer
	best_offer = {} # only trade to get an offer better than current best

	# go through each student and add edges to all schools better than current best
	nodes = {}
	for student in students:
		# find best current offer
		for i in xrange(len(student.rankings)):
			school = student.rankings[i]
			if student in tent_offers[school]:
				best_offer[student] = i
				break
		# add edges to all schools that aren't full and are better than current best
		# edge should be (school, student with offer)
		if student in best_offer:
			nodes[student] = []
			#for i in xrange(best_offer[student] - 1): 
			for i in xrange(best_offer[student]): 
				school = student.rankings[i]
				nodes[student].extend([(school, offer) for offer in tent_offers[school] if school not in full_schools])
			for school in tent_offers_student[student]:
				graph[(school, student)] = nodes[student]
	return graph

def force_assignments():
	for student in students:
			tent_offers_student[student] = set()
	for school in schools:
		tent_offers[school.name] = []
	for school in schools:
		print "-----------"
		print school.name
		print school.capacity
		print len(assignments[school.name])
		print len(tent_offers[school.name])
		print school.name in full_schools
		print school in full_schools
		print "-----------"
	# offers_removed = 0
	# for student in students:
	# 	if student not in assigned_students and len(tent_offers_student[student]) > 0:
	# 		print "force_assignments for " + student
	# 		for i in xrange(len(student.rankings)):
	# 			school = student.rankings[i]
	# 			if student in tent_offers[school]:
	# 				break
	# 		assignments[school].append(student)
	# 		assigned_students.add(student)
	# 		offers = tent_offers_student[student]
	# 		offers_removed += len(offers) -1
	# 		for sch in offers:
	# 			tent_offers[sch].remove(student)
	# 		if len(assignments[school]) == capacities[school]:
	# 			 full_schools.add(school)


def remove_cycles():
	graph = make_pref_graph()

	# start doing dfs to find loops, each student is a vertex
	# need to keep track of path so we can call trade_cycle and deletes
	visited_students1  = set()
	backtrack = {} # (school, student) --> (prev_school, prev_student)
	#prev_student = None

	broke_a_cycle = False
	ct = 0
	for school, student in graph:
		ct += 1
		backtrack = {}
		if (school, student) not in visited_students1:
			visited_students  = set()
			visited_students1.add((school, student))
			visited_students.add((school, student))
			backtrack[(school, student)] = None
			to_visit = [((school, student), next) for next in graph[(school, student)]]
			#prev_student = student
			while len(to_visit) != 0:
				prev, cur = to_visit.pop()
				backtrack[cur] = prev
				sch, stud = cur
				if (sch, stud) in graph:
					if (sch, stud) in visited_students:
						#print "found school again"
						#print sch
						result = trade_cycle(backtrack, stud, sch)
						if result:
							return True
					visited_students.add((sch, stud))
					to_visit.extend([((sch, stud), next) for next in graph[(sch, stud)]])
	return broke_a_cycle

def remove_cycles1():
	graph = make_pref_graph()


loop_round = 1
found_cycles = True
new_cap = 1

# restart sim
while num_assigned < num_students:
	# schools make offers to students
	print "-------------"
	print "num_assigned = " + str(num_assigned) + ", round = " + str(loop_round) 
	prev_assigned = -1
	while prev_assigned < num_assigned:
		print "offering"
		prev_assigned  = num_assigned
		new_cap = make_offers()
		accept_offers()
		num_assigned = len(assigned_students)
	print "num_assigned = " + str(num_assigned)
	cycles = True
	iters = 0
	while(cycles) and iters < 3:
		iters += 1
		print "removing cycles"
		cycles = remove_cycles()
		print cycles
		prev_assigned = len(assigned_students)
		accept_offers()
		num_assigned = len(assigned_students)
		if prev_assigned != num_assigned:
			break
		#else:
		#	iters -= 1
		print "num_assigned = " + str(num_assigned)
	new_cap = make_offers()
	if new_cap == 0 and not cycles:
		print "forcing_assignments"
		force_assignments()
	loop_round += 1
	# for school in assignments:
	# 	print
	# 	print school
	# 	print [s.race for s in assignments[school]]

	# some students accept offers (loop until no more do)
	# remove cycles
	# some students accept offers (loop until no more do)

for school in assignments:
	print
	print school
	print [s.race for s in assignments[school]]

pkl.dump(assignments, open("assignments1.p", "wb"))
