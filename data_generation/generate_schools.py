from student import School
import random as rand
import pickle as pkl
import copy


f = open("school_caps.csv")

def get_all_schools():
	schools = {}
	for line in f:
		line = line.split(",")
		if str(line[1]).strip() != 'GEN':
			name = str(line[0]).strip() + str(line[1]).strip()
		else:
			name = str(line[0]).strip()
		cap = int(line[2])
		print name, cap
		s = School(name,cap)
		schools[s] = s
	return schools


schools = get_all_schools()
pkl.dump(schools, open("schools.p", "wb"))






