# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 14:39:40 2018

@author: Timothy_Richards
"""

import hf_main_dataprep
import hf_flux_calc
import hf_flux_plots
#%%
#Prepare raw data for analysis
hf_main_dataprep()
#Calculate fluxes
hf_flux_calc()
#Flux plots
hf_flux_plots()
