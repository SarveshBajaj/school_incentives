from student import Student
import random as rand
import pickle as pkl
import copy


f = open("census_tract.csv")
standard_score = pkl.load(open("scores.p", "rb"))
types = pkl.load(open("school_type.p", "rb"))


def get_all_students():
	students = []
	for line in f:
		line = line.split(",")
		#ct = str(line[0])
		ct = line[2]
		if ct == 'CTIP':
			continue
		schools = str(line[1])
		schools = schools.split('/')
		s_probs = []
		school_names = []
		for school in schools:
			school_prob = school.split(' 0')
			school_names.append(school_prob[0])
			if len(school_prob) > 1:
				s_probs.append(float(school_prob[1]))
			else:
				s_probs.append(1.0)

		kgers = round(float(line[16]))
		hisp = round(float(line[17]))
		white = round(float(line[19]))
		black = round(float(line[20]))
		amind = round(float(line[21]))
		asian = round(float(line[22]))
		nathaw = round(float(line[23]))
		multi = round(float(line[25]))
		kgers =  (hisp + white + black + amind + asian + nathaw + multi)
		for i in range(int(kgers)):
			s = Student()
			s.ct = ct
			sp = rand.random()
			prob = s_probs[0]
			sch = ''
			if len(s_probs) == 1 or sp <= prob:
				sch = school_names[0]
			else:
				sch = school_names[1]
			s.att_area = sch.strip()
			if hisp > 0:
				s.race = 'hisp'
				hisp -=1
			elif white > 0:
				s.race = 'white'
				white -=1
			elif black > 0:
				s.race = 'black'
				black -=1
			elif amind > 0:
				s.race = 'amind'
				amind -=1
			elif asian > 0:
				s.race = 'asian'
				asian -=1
			elif nathaw > 0:
				s.race = 'nathaw'
				nathaw -=1	
			elif multi > 0:
				s.race = 'multi'
				multi -=1
			else:
				s.race = 'asian'

			score  = copy.deepcopy(standard_score) # add variance
			score[s.att_area] += max(rand.normalvariate(1000, 100), 0.1)
			immersion_pref = max(min(rand.normalvariate(1, 0.5), 1), 0.1)
			for school in types:
				if types[school] != "GEN":
					score[school] *= immersion_pref
			total_score = 0
			for school in score:
				total_score += score[school]
			rankings = []
			while len(score) > 0:
				#print score
				p = rand.random()
				cumulative_prob = 0
				for school in score:
					#print score[school] 
					#print total_score
					cumulative_prob += (score[school] / total_score)
					if cumulative_prob > p:
						rankings.append(school)
						total_score -= score[school]
						del score[school]
						break
			s.rankings = rankings
			if s.ct == 1:
				s.private_schoool_cutoff = len(s.rankings) + 1
			else:
				s.private_schoool_cutoff = rand.randint(0, len(s.rankings))
			students.append(s)
	return students


students =  get_all_students()
# ranking_map = {}
# for student in students:
# 	for i in xrange(len(student.rankings)):
# 		school = student.rankings[i]
# 		if school not in ranking_map:
# 			ranking_map[school] = [0 for i in xrange(8)]
# 		ranking_map[school][min(i, 7)] += 1
# for school in ranking_map:
# 	print school
# 	print ranking_map[school]
# 	print

# print ranking_map['Clarendon']
# print ranking_map['Carver']



pkl.dump(students, open("students.p", "wb"))






