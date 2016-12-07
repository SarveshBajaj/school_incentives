import random
import copy
import pickle as pkl
from student import Student,School
students = pkl.load(open("students.p", "rb"))
schools = pkl.load(open("schools.p", "rb"))

students = random.sample(students, int(round(len(students) / 10.0)  - 1))

tent_offers = {}
tent_offers_student = {}
assignments = {}
assigned_students = set()
unassigned_students = []
capacities = {}
full_schools = set()


#students = random.sample(students, int(round(len(students) / 10.0)))

for school in schools:
 	school.capacity /= 10.0
 	school.capacity = int(round(school.capacity))

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

def fix_students():

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
def initialize():
	for school in schools:
		tent_offers[school.name] = []
		assignments[school.name] = []
		capacities[school.name] = school.capacity

	for student in students:
		tent_offers_student[student] = set()
	unassigned_students = [student for student in students]

def make_pref_graph():
	#print "REMAKING GRAPH"
	graph = {} # (school, student) --> (school, student) where student has offer at school which is better than current best offer
	best_offer = {} # only trade to get an offer better than current best

	# go through each student and add edges to all schools better than current best
	nodes = {}
	for student in unassigned_students:
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
				nodes[student].extend([(school, offer) for offer in tent_offers[school] if school not in full_schools and offer in unassigned_students])
			#if len(nodes[student]) > 0:
			for school in tent_offers_student[student]:
				graph[(school, student)] = nodes[student]
	return graph

def is_cycle(backtrack, pair):
	cur = pair
	prev = backtrack[pair]
	while(prev != pair):
		cur = prev
		if cur not in backtrack:
			return False
		prev = backtrack[cur]
	return True


def break_cycle(end, backtrack):
	print "CYCLE"
	i = 0
	prev = backtrack[end]
	if prev is None:
			print "NONE:"
			print backtrack
			print cur
	cur = end
	while prev != end:
		i += 1
		cur_school, cur_student = cur 
		prev_school, prev_student = prev 
		tent_offers[cur_school].remove(cur_student)
		tent_offers[cur_school].append(prev_student)

		tent_offers_student[cur_student].remove(cur_school)
		tent_offers_student[prev_student].add(cur_school)

		cur = prev
		#if cur not in backtrack:
		#	print end
		#	print backtrack
		prev = backtrack[cur]
		if prev is None:
			print "NONE:"
			print backtrack
			print cur
	cur_school, cur_student = cur 
	prev_school, prev_student = prev 
	tent_offers[cur_school].remove(cur_student)
	tent_offers[cur_school].append(prev_student)

	tent_offers_student[cur_student].remove(cur_school)
	tent_offers_student[prev_student].add(cur_school)
	#print "BROKE CYCLE"
	return True

def DFS(vertex, time, color, discovery_time, finishing_time, p,graph):
	color[vertex] = "GRAY"
	discovery_time[vertex] = time
	time += 1
	for v in graph[vertex]:
		if v in color:
			if color[v] == "WHITE":
				p[v] = vertex
				dfs_time = DFS(v, time, color, discovery_time, finishing_time, p, graph) 
				if dfs_time < 0:
					return dfs_time
				time = dfs_time + 1
			# otherwise cycle
			elif color[v] == "GRAY":
				#print "LOOP"
				p[v] = vertex
				break_cycle(vertex, p)
				return -1
	finishing_time[vertex] = time
	color[vertex] = "BLACK"
	return finishing_time[vertex]

def remove_cycles_color():
	new_graph = True
	num_cycles = 0
	while new_graph:
		graph = make_pref_graph()
		new_graph = False
		colors = {}
		discovery_time = {}
		finishing_time = {}
		p = {}
		for vertex in graph:
			colors[vertex] = "WHITE"
			discovery_time[vertex] = float('Inf')
			finishing_time[vertex] = float('Inf')
			p[vertex] = None
		time = 1
		for vertex in graph:
			#print vertex
			#print colors[vertex]
			if colors[vertex] == "WHITE":
				result = DFS(vertex, time, colors, discovery_time, finishing_time, p,graph)
				if result < 0:
					new_graph = True
					num_cycles += 1
					accept_matches()
					break
				time = result + 1
	return num_cycles

# remove all cycles in graph, return num cycles removed
def remove_cycles():
	#print "removing cycles"
	num_cycles = 0
	visited_pairs = set()
	new_graph = True
	while new_graph:
		graph = make_pref_graph() # (school, student)  ---> [(school, student), ] preferred
		new_graph = False
		for pair in graph:
			if pair not in visited_pairs:
				print
				print pair
				backtrack = {} # sch1, stud1 ---> stud2 that prefers sch1
				visited_nodes = set()
				visited_nodes.add(pair)
				visited_pairs.add(pair)
				to_visit = [pair]
				to_visit.extend([(pair, next) for next in graph[pair]])

				finished_index = {}
				finished_index[pair] = 0
				while len(to_visit) != 0:
					prev, cur = to_visit.pop()
					if cur in finished_index and (len(to_visit) - 1) > finished_index[cur]:
						print "finished_index"
						print finished_index[cur]
						print (len(to_visit) - 1) 
						backtrack[cur] = prev
						break_cycle(cur, backtrack)
						new_graph = True
						break

							# cycle
					elif cur in graph: # not cycle
						backtrack[cur] = prev
						finished_index[cur] = len(to_visit)
						visited_nodes.add(cur)
						visited_pairs.add(cur)
						to_visit.extend([(cur, next) for next in graph[cur]])
					# add to finished


					#if cur not in visited_nodes and cur != pair:
					# visited_pairs.add(cur)
					# backtrack[cur] = prev
					# #backtrack[prev] = cur
					# if cur in graph:
					# 	if cur in visited_nodes: # should mean someting prefers cur
					# 		num_cycles += 1
					# 		break_cycle(cur, backtrack)
					# 		new_graph = True
					# 	else:
					# 		visited_nodes.add(cur)
					# 		visited_pairs.add(cur)
					# 		to_visit.extend([(cur, next) for next in graph[cur]])
					# 	if new_graph:
					# 		break
			if new_graph:
				break
	print "num_cycles = " + str(num_cycles)
	return num_cycles


# returns number of offers made
def make_tentative_offers():
	offers_made = 0
	num_unassigned = len(students) - len(assigned_students) 
	if num_unassigned == 0:
		return offers_made
	for school in schools:
		if school not in full_schools:
			open_space = school.capacity - len(tent_offers[school.name]) - len(assignments[school.name])
			open_space = min(open_space, num_unassigned)
			if open_space > 0:
				ctip = []
				aa = []
				other = []
				for student in unassigned_students:
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
				offers.extend(ctip[0:open_space])
				if len(offers) < open_space:
					offers.extend(aa[0:(open_space - len(offers))])
				if len(offers) < open_space:
					offers.extend(other[0:(open_space - len(offers))])
				tent_offers[school.name].extend(offers)
				for offer in offers:
					offers_made += 1
					tent_offers_student[offer].add(school.name)
	return offers_made


# return num spots opened by accepting match
def accept_match(student, school):
	spots_opened = len(tent_offers_student[student]) - 1
	unassigned_students.remove(student)
	assigned_students.add(student)
	assignments[school].append(student)
	for school in tent_offers_student[student]:
		tent_offers[school].remove(student)
	del tent_offers_student[student]
	if len(assignments[school]) == capacities[school]:
		full_schools.add(school)
	return spots_opened


# students accepted to top choice accept assignment
# returns number spaces opened as a result (true if students accept offers)
def accept_matches():
	spots_opened = 0
	for student in unassigned_students:
		first_empty = -1
		for i in xrange(len(student.rankings)):
			if student.rankings[i] not in full_schools:
				first_empty = i
				break
		if first_empty >= 0:
			school = student.rankings[first_empty]
			if school in tent_offers_student[student]:
				spots_opened += accept_match(student, school)
	return spots_opened

def force_assignments():
	print "force_assignments"
	result = False
	for student in unassigned_students:
		first_empty = -1
		for i in xrange(len(student.rankings)):
			if student.rankings[i] in tent_offers_student[student]:
				first_empty = i
				break
		if first_empty >= 0:
			result = True
			school = student.rankings[first_empty]
			accept_match(student, school)
		else:
			print "NO MATCH"
	return result


def run_simulation():
	print len(unassigned_students)
	num_offers = 1
	tentative_space = 1
	i = 1
	cur_unassigned = len(unassigned_students) 
	prev_unassigned = len(unassigned_students) + 1
	num_cycles = 1
	while num_cycles > 0 or cur_unassigned < prev_unassigned:
		prev_unassigned = cur_unassigned
		i += 1
		while tentative_space > 0:
			num_offers = make_tentative_offers() # this fills all tentative offer spots for each school (or assigns all students)
			print "num offers: " + str(num_offers)
			if num_offers == 0:
				break
			tentative_space = accept_matches() # now there might be more available tenative spots
		#num_cycles = remove_cycles()
		num_cycles = remove_cycles_color()
		print "CYCLES: " + str(num_cycles)
		#if num_cycles > 0:
		make_tentative_offers()
		accept_matches()
		cur_unassigned = len(unassigned_students) 
	make_tentative_offers()
	accept_matches()
	while(len(unassigned_students) > 0):
		worked = force_assignments()
		if not worked:
			break



fix_students()
#test_students()
initialize()
unassigned_students = [student for student in students]
run_simulation()
print
# print assignments


# for school in assignments:
# 	print
# 	print school
# 	print [s.att_area for s in assignments[school]]
# 	print [s.att_area for s in tent_offers[school]]

# for school in assignments:
# 	print "------"
# 	print school
# 	print capacities[school]
# 	print len(assignments[school])
# 	print len(tent_offers[school])

print len(assigned_students)
print len(unassigned_students)
print len(students)

pkl.dump(assignments, open("assignments10percent.p", "wb"))


