# SFUSD Matching System Incentives
### CS269i Group Project: Ambika A., Sarah R., Tara B.

### Description
Implementations of the SFUSD matching system process on data we generated ourselves using various data sources published by the SFUSD. This repositroy include: the .pdf of our report, where you can learn more about the project, how we generated our data and our findings, and directories which split up our codebase.

### Directory Structure
data/ contains SFUSD data on census tracts, demographics, school capacities, etc.
data_generation/ includes scripts to aggregate SFUSD data to create our students so they reflect the data distributions we researched
extra_work/ includes the many different simulations and things we tried throughout this project before we settled on our most optimized and correct simulations
metrics/ contains scripts to run aggregate statistics and generate visualizations of our results
open_source/ contains files we tried from a similar open source project(see: https://github.com/ogaway/Matching-Market/blob/master/matchfuncs.py)
pickled_data/ contains stored data structures we generated of student and school objects
results/ includes the results of our various simulations on different sample sizes
simulations/ contains models for the current SFUSD system, and a lottery draw based system
student.py is the Student objct class