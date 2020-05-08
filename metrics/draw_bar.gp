set style data histograms

set boxwidth 0.8
set style fill solid

plot "draw_plot.dat" using 2:xtic(1) title "Racially Isolated" lt rgb "#6255ed","" using 3 title "First Choice" lt rgb "#7bed77","" using 4 title "AA" lt rgb "#bd7f2f"