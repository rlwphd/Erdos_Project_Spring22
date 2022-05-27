# MiceKinematics

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)

This notebook allows the user to analyze the EMG and kinematic data created when either running a mouse on the treadmill or air stepping a pup.
This notebook is designed to be run on Google Colab making use of their free GPU services. It may be run on a local machine using juypter notebook or juypter lab.

For the kinematic analysis, this notebook uses a combination of DeepLabCut for tracking bodyparts and in house kinematic analysis to create phase plots and joint angles during movement.

For the EMG analysis, this notebook uses in house analysis to analyze timing of activity based on the step cycle from the kinematic analysis and generates phase plots.