import random
import copy
import pickle as pkl
from student import Student,School
students = pkl.load(open("students.p", "rb"))
schools = pkl.load(open("schools.p", "rb"))

tent_offers = {} # school name --> student
assignments = {} # school name --> student
full_schools = [] # school name
capacities = {}
assigned_students = set()
num_assigned = 0

for student in students:
	for i in xrange(len(student.rankings)):
		if student.rankings[i] == "AlvaraoIMMS":
			student.rankings[i] = "AlvaradoIMMS"
		if student.rankings[i] == "King":
			student.rankings[i] = "Starr King"
		if student.rankings[i] == "KingIMMM":
			student.rankings[i] = "Starr KingIMMM"

for school in schools:
	tent_offers[school.name] = []
	assignments[school.name] = []
	capacities[school.name] = school.capacity

# keep going until all are assign (add cycle part)
while num_assigned < len(students):
	print "num_assigned = " + str(num_assigned)
	print full_schools
	# for each school, give out more tentative assignments so len(tentative assignments) = capacity
	for school in schools:
		assignments[school] = []
		ctip = []
		aa = []
		other = []
		# go through all unassigned student and break into priority groups to make offers
		for student in students:
			if student not in assigned_students:
				if school.name in student.rankings: #and student.rankings.index(school.name) < student.private_schoool_cutoff:
					if int(student.ct) == 1:
						ctip.append(student)
					elif student.att_area == school.name:
						aa.append(student)
					else:
						other.append(student)
		# make in-group selections a random lottery
		random.shuffle(ctip)
		random.shuffle(aa)
		random.shuffle(other)
		#if len(aa) == 0:
		#	print "no att_area"
		#	print school.name
		#	print
		offers = []
		# print school.name
		# print school.capacity
		# print len(ctip[0:school.capacity])

		# make offers so ten_offers = capacity
		cap_remaining = school.capacity - len(tent_offers[school.name])
		offers.extend(ctip[0:cap_remaining])
		if len(offers) < cap_remaining:
			offers.extend(aa[0:(cap_remaining - len(offers))])
		if len(offers) < cap_remaining:
			offers.extend(other[0:(cap_remaining - len(offers))])
		# print "-------"
		# print school.capacity
		# print cap_remaining
		# print len(offers)
		# print len(tent_offers[school.name])
		# print "-------"
		tent_offers[school.name].extend(offers)

	#names = [school.name for school in schools]
	#print names

	# assign all students who have an offer at their top remaining choice
	for student in students:
		if student not in assigned_students:
			# find 1st not full
			first_empty = -1
			for i in xrange(len(student.rankings)):
				if student.rankings[i] not in full_schools:
					first_empty = i
					break
			if first_empty >= 0:
				#if student.rankings[first_empty] not in tent_offers:
				#	print student.rankings[first_empty]
				#else:
				school = student.rankings[first_empty]
				top_assignments = tent_offers[school]
				#print student.rankings[first_empty]
				if student in top_assignments:
					# accept offer
					if school not in assignments:
						assignments[school] = []
					assignments[school].append(student)
					assigned_students.add(student)
					num_assigned += 1
					tent_offers[school].remove(student)
					if len(assignments[school]) == capacities[school]:
						 full_schools.append(school)

# make graph and find cycles
	graph = {} # student --> edges
	visited_students  = set()
	best_offer = {}
	for student in students:
		for i in xrange(len(student.rankings)):
			school = student.rankings[i]
			if student in tent_offers[school]:
				best_offer[student] = i
				break

	# add ptr to all schools above i
	for student in student:
		edges = []
		for i in xrange(best_offer[student] - 1):
			# add edge to each student w/ offer to that school, keep name of school
			school = student.rankings[i]
			new_edges = [(school, offer) for offer in tent_offers[school]]
			edges.extend(new_edges)
		graph[students] = edges
	for student in students:
		visited = set()
		prev = {} #student -> prev
		to_visit = copy.deepcopy(edges)
		while len(to_visit) > 0:
			next = []
			for school, offer in to_visit:
				if offer not in visited and offer != student:
					visited.add(offer)
					next.append((school, offer))

		



	#print tent_offers
for school in schools:
	print "-----------"
	print school.name
	print school.capacity
	print len(assignments[school.name])
