# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 14:39:40 2018

@author: Timothy_Richards

Description:
"""

import hf_main_dataprep
import hf_flux_calc
import hf_flux_plots
import hf_plots
#%%
#Prepare raw data for analysis
hf_main_dataprep()
#Calculate fluxes
hf_flux_calc()
#Flux plots
hf_flux_plots()
#Other plots
#Call all plots seperately from hf_plots
hf_plots.scatter_windspd()
#
