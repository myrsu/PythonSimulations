# Analyzing simulation results pipeline


## Description

The goal is to give a simple understanding & overview of my way of analyzing raw data from particles-in-cell [Smilei](https://smileipic.github.io/Smilei/index.html) simulations.
Even though Smilei has a built-in library for postprocessing the data, you may prefer to extract raw data first because you can implement more advanced analysis with a script built by yourself.



## Pipeline

1. [Create a namelist.](https://smileipic.github.io/Smilei/Use/namelist.html)
2. [Start your simulation.](https://smileipic.github.io/Smilei/Use/run.html)
3. Run .py script to extract your data into the shelve file. You can use the shelving.py file as an example.
4. Run .py script to analyze extracted data. You can use post_shelving.py as an example. If you want to use it - you need **edit** it first since this file is not for instant use.
