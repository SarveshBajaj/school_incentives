import csv
import pickle as pkl

school, aa, code, first, second, third, fourth, fifth, sixth, seventh, eighth = (0,1,2,4,5,6,7,8,9,10,11)
#points for each ranking
pts = [100, 80, 70, 60, 50, 40, 30, 20]

def calculate_score(rankings):
	rankings = [int(rank) for rank in rankings]
	print rankings
	score = 0
	for i in xrange(len(rankings)):
		score += (rankings[i] * pts[i])
	print score
	return score


# returns a list of schools
# school name(+Code), score
# returns a dict of school, type
def get_school_scores():
	with open('School_Prefs.csv', 'rb') as pref_file:
		csv_reader = csv.reader(pref_file, delimiter=',', quotechar='|')
		titles = None
		scores = {}
		types = {}
		for row in csv_reader:
			if not titles:
				titles = row
			else:
				name = row[school]
				school_type = row[code]
				if school_type != "GEN":
					name += school_type
				types[name] = school_type
				print name
				scores[name] = calculate_score(row[first:eighth])

	return(scores, types)

scores, types = get_school_scores()
pkl.dump(scores, open("scores.p", "wb"))
pkl.dump(types, open("school_type.p", "wb"))
print scores
print types