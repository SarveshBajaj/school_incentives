import student
import random as rand

f = open("census_tract.csv")

def get_all_students():
	students = []
	for line in f:
		line = line.split(",")
		ct = str(line[0])
		if ct == 'Census Tract':
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
		hisp = round(float(line[18]))
		white = round(float(line[19]))
		black = round(float(line[20]))
		amind = round(float(line[21]))
		asian = round(float(line[22]))
		nathaw = round(float(line[23]))
		multi = round(float(line[25]))

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
			s.att_area = sch
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
		students.add(s)
	return students










