from random import random

class Student:
	def __init__(self,census_tract,closest):
		self.ct = census_tract
		self.closest_schools = closest
		self.rankings = None
		self.private_schoool_pref = None
		self.p_shift = 0.1

	def set_ranking(self, standard_ranking):
		self.rankings = standard_ranking
		for i in xrange(len(standard_ranking) - 1):
			p = random()
			#change p_shift to be higher if neighborhood, change for immersion
			if p < self.p_shift:
				temp = self.rankings[i]
				self.rankings[i] = self.rankings[i + 1]
				self.rankings[i + 1] = temp



# try adding in a pref for similar race?

# ranking fn
# start with standard prefs   -- should we separate 
# p(shift) [0,1]
# immersion pref strength [-1,1]

# also h






# score (school) 100 * num 1st 

# add points for immersion -- normal(30, 70)

# add for close -- normal(30, 70)

# p(ranking next) = score / (total score left)



