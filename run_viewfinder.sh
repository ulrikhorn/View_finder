#bash

# Argument start coordinates
## Parse

# check if coordinate df already exsists
# if not run:
mkdir results_folder 

python ielevation.py -args

# Check that df is generated

Rscript view_plotter

# open html 