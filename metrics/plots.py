import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
import pandas as pd
import os

file1 = open("draw_plot.dat","a")
file1.seek(0)
file1.truncate()
file1.close()

assignments = pkl.load(open("../results/draw_assignments.p","r"))
current = pkl.load(open("../results/assignments10percent.p","r"))
flipped = pkl.load(open("../results/assignments10-flipped.p","r"))

to_plot_draw = {}
to_plot_current = {}
to_plot_flipped = {}

num_students_first_draw = 0
num_students_first_current = 0
num_students_first_flipped = 0
num_att_area_draw = 0
num_att_area_current = 0
num_att_area_flipped = 0
studs_draw = 0
studs_current = 0
studs_flipped = 0

for school in assignments:
	tot_students_draw = len(assignments[school])
	races_draw = {}
	for student in assignments[school]:
		studs_draw +=1
		if student.att_area == school:
			num_att_area_draw +=1
		if student.rankings[0] == school:
			num_students_first_draw +=1
		student_race = student.race
		if student_race not in races_draw:
			races_draw[student_race] = 0
		races_draw[student_race] +=1
	for r in races_draw:
		if races_draw[r]/float(tot_students_draw) >= 0.6 and races_draw[r]/float(tot_students_draw) < 1.0:
			to_plot_draw[school] = races_draw
			break

for school in current:
	tot_students_current = len(current[school])
	races_current = {}
	for student in current[school]:
		studs_current +=1
		if student.att_area == school:
			num_att_area_current +=1
		if student.rankings[0] == school:
			num_students_first_current +=1
		student_race = student.race
		if student_race not in races_current:
			races_current[student_race] = 0
		races_current[student_race] +=1
	for r in races_current:
		if races_current[r]/float(tot_students_current) >= 0.6 and races_current[r]/float(tot_students_current) < 1.0:
			to_plot_current[school] = races_current
			break

for school in flipped:
	tot_students_flipped = len(flipped[school])
	races_flipped = {}
	for student in flipped[school]:
		studs_flipped +=1
		if student.att_area == school:
			num_att_area_flipped +=1
		if student.rankings[0] == school:
			num_students_first_flipped +=1
		student_race = student.race
		if student_race not in races_flipped:
			races_flipped[student_race] = 0
		races_flipped[student_race] +=1
	for r in races_flipped:
		if races_flipped[r]/float(tot_students_flipped) >= 0.6 and races_flipped[r]/float(tot_students_flipped) < 1.0:
			to_plot_flipped[school] = races_flipped
			break

print "number of schools with 60-percent of one race",len(to_plot_draw)
print "number of students who got their first choice:",num_students_first_draw/float(studs_draw)
print "number of students who got their att_area school:",num_att_area_draw/float(studs_draw)

file1 = open("draw_plot.dat","a")
file1.write("{} {} {} {}\n".format("Current",len(to_plot_current)/float(100),num_students_first_current/float(studs_current) ,num_att_area_current/float(studs_current)))
file1.write("{} {} {} {}\n".format("Flipped",len(to_plot_flipped)/float(100),num_students_first_flipped/float(studs_flipped) ,num_att_area_flipped/float(studs_flipped)))
file1.write("{} {} {} {}\n".format("Draw",len(to_plot_draw),num_students_first_draw/float(studs_draw) ,num_att_area_draw/float(studs_draw)))
file1.close()
os.system('cmd /k "gnuplot -persist draw_bar.gp"')
# #plotting
# schools = [x for x in to_plot][7:14]
# white_students = [to_plot[x]['white']/float(sum(to_plot[x].values())) if 'white' in to_plot[x] else 0 for x in to_plot][7:14]
# black_students = [to_plot[x]['black']/float(sum(to_plot[x].values())) if 'black' in to_plot[x] else 0 for x in to_plot][7:14]
# asian_students = [to_plot[x]['asian']/float(sum(to_plot[x].values())) if 'asian' in to_plot[x] else 0 for x in to_plot][7:14]
# hisp_students = [to_plot[x]['hisp']/float(sum(to_plot[x].values())) if 'hisp' in to_plot[x] else 0 for x in to_plot][7:14]
# nathaw_students = [to_plot[x]['nathaw']/float(sum(to_plot[x].values())) if 'nathaw' in to_plot[x] else 0 for x in to_plot][7:14]
# multi_students = [to_plot[x]['multi']/float(sum(to_plot[x].values())) if 'multi' in to_plot[x] else 0 for x in to_plot][7:14]
# amind_students = [to_plot[x]['amind']/float(sum(to_plot[x].values())) if 'amind' in to_plot[x] else 0 for x in to_plot][7:14]

# width = 0.35
# N = len(schools)
# ind = np.arange(N)
# wh = plt.bar(ind, white_students, width)
# bl = plt.bar(ind, black_students, width,bottom = white_students)
# asn = plt.bar(ind, asian_students, width, bottom = white_students+ black_students)
# hisp = plt.bar(ind, hisp_students, width, bottom = white_students + black_students + asian_students)
# nh = plt.bar(ind, nathaw_students, width, bottom = white_students + black_students + asian_students + hisp_students)
# mul = plt.bar(ind, multi_students, width, bottom = white_students + black_students + asian_students + hisp_students + nathaw_students)
# amin = plt.bar(ind, amind_students, width, bottom = white_students + black_students + asian_students + hisp_students + nathaw_students + multi_students)

# #Set the label and legends
# plt.ylabel("Percentages of race")
# plt.xlabel("School with greater than 60percent of one race")
# # plt.legend(loc='upper left')
# plt.xticks(ind+width/2., schools)
# plt.yticks(np.arange(0,100,25))
# plt.show()
# raw_data = {'school': [x for x in to_plot][7:14],
#         'white': [to_plot[x]['white']/float(sum(to_plot[x].values())) if 'white' in to_plot[x] else 0 for x in to_plot][7:14],
#         'black': [to_plot[x]['black']/float(sum(to_plot[x].values())) if 'black' in to_plot[x] else 0 for x in to_plot][7:14],
#         'asian': [to_plot[x]['asian']/float(sum(to_plot[x].values())) if 'asian' in to_plot[x] else 0 for x in to_plot][7:14],
#         'hisp': [to_plot[x]['white']/float(sum(to_plot[x].values())) if 'white' in to_plot[x] else 0 for x in to_plot][7:14],
#         'nathaw': [to_plot[x]['black']/float(sum(to_plot[x].values())) if 'black' in to_plot[x] else 0 for x in to_plot][7:14],
#         'multi': [to_plot[x]['asian']/float(sum(to_plot[x].values())) if 'asian' in to_plot[x] else 0 for x in to_plot][7:14],
#         'amind': [to_plot[x]['white']/float(sum(to_plot[x].values())) if 'white' in to_plot[x] else 0 for x in to_plot][7:14]}
# df = pd.DataFrame(raw_data, columns = ['school', 'white', 'black', 'asian','hisp','nathaw','multi','amind'])

# f, ax1 = plt.subplots(1, figsize=(10,5))

# bar_width = 0.25
# bar_l = [i+1 for i in range(len(df['white']))] 

# tick_pos = [i+(bar_width/2) for i in bar_l]
# # Create a bar plot, in position bar_1
# wh = plt.bar(bar_l, 
#         # using the pre_score data
#         df['white'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='White', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='#f26b38')

# bl = plt.bar(bar_l, 
#         # using the pre_score data
#         df['black'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='Black', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='#f7db4f')

# asn = plt.bar(bar_l, 
#         # using the pre_score data
#         df['asian'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='Asian', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='#a7226e')

# hisp = plt.bar(bar_l, 
#         # using the pre_score data
#         df['hisp'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='Hispanic', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='#ec2035')

# multi = plt.bar(bar_l, 
#         # using the pre_score data
#         df['multi'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='Multiracial', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='#2f9599')

# amind = plt.bar(bar_l, 
#         # using the pre_score data
#         df['amind'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='American Indian', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='b')

# nathaw = plt.bar(bar_l, 
#         # using the pre_score data
#         df['nathaw'], 
#         # set the width
#         width=bar_width,
#         # with the label pre score
#         label='Native Hawaiian', 
#         # with alpha 0.5
#         alpha=0.5, 
#         # with color
#         color='w')


# # set the x ticks with names
# plt.xticks(tick_pos, df['school'])

# # Set the label and legends
# plt.ylabel("Percentages of race")
# plt.xlabel("School with greater than 60percent of one race")
# plt.legend(loc='upper left')

# # Set a buffer around the edge
# plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])


# plt.show()

