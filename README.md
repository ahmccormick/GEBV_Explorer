#############
# 🧬 GEBV Explorer
# An app to interactively filter and visualize genomic estimated breeding values (GEBVs)
#############

#############
#First Steps to download and run GEBV Explorer
#Clone the repo with the below command in terminal
git clone https://github.com/ahmccormick/GEBV_Explorer.git
cd GEBV_Explorer


#Install dependencies (made using python 3.12.10)
pip install -r requirements.txt

#Launch the app
streamlit run GEBV_app_6.py


#############
#Data 

#App contains the GEBV data for 13 agronomic traits and 16 quality traits for the Capsicum core collection (n=423)
#16 quality trait data located in: data/GEBV_quality_core_16traits_n423.csv
#13 agronomic traits (averaged over three experimental timepoints) located in: data/GEBVs_core_13_agronomic_traits_avg.csv


#############
#Usage

# Adjust sliders on the left to filter lines for any GEBV trait or combinations of traits
# The filtered table will update in real time.
# Explore any two-trait combinations in the scatterplot (default: Yield vs. Brix)
# Red points in the scatterplot highlight the lines that meet all of your threshold criteria
# Download filtered lines as a CSV.