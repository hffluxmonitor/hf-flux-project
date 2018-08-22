# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 13:03:09 2018

@author: FluxMonitor
"""
import dropbox

API_key = 'DUEgEelOH7AAAAAAAAAALll6OKnnPNyGgBcjBjhcPJjiwDJQGzHz5OJoponmSl8Z'
dbx = dropbox.Dropbox('DUEgEelOH7AAAAAAAAAALll6OKnnPNyGgBcjBjhcPJjiwDJQGzHz5OJoponmSl8Z')

dbx.get_file('Obrist Lab/HarvardForestData/flux_data.csv')