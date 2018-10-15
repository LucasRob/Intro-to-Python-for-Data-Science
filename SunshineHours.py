#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#Create sunshine dataFrame and converting -9999.9 values into NaN
sun = pd.read_csv('sunshine.csv', index_col=False, na_values = -9999.9)

#We use only the WMO Station Number and the Annual mean column
sun = sun.loc[:,['WMO Station Number','Annual NCDC Computed Value']]
sun = sun.rename(columns={'WMO Station Number': 'WMO', 'Annual NCDC Computed Value': 'Annual Mean'})
sun = sun.dropna(axis = 0)
sun['WMO'] = sun['WMO'].apply(int)

#We read from mlid the WMO stations and its coordinates for plotting
mlid = pd.read_csv('mlid-20180925_public-2.csv', index_col=False, usecols=['wmo', 'lat_prp', 'lon_prp'])
mlid = mlid.rename(columns={'wmo': 'WMO', 'lat_prp':'LAT', 'lon_prp': 'LON'})
mlid = mlid.dropna(axis = 0)
mlid['WMO'] = mlid['WMO'].apply(int)

#We join the two Dataframes using the WMO column
sun = sun.set_index('WMO').join(mlid.set_index('WMO'))

sun['LAT'] = sun['LAT'].replace('', np.nan)
sun['LON'] = sun['LON'].replace('', np.nan)
sun = sun.dropna(axis = 0)

lat = sun['LAT'].values
lon = sun['LON'].values
annualMean = sun['Annual Mean'].values

fig = plt.figure(figsize=(10, 10))
#Create BaseMap with Miller Projection
map = Basemap(projection='mill', 
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180)

# Plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
# Fill continents with eggshell ffffd4 color 
map.drawmapboundary(fill_color='#ffffd4')

# Create the scatter plot using inferno colormap
map.scatter(lon, lat, latlon=True,
          c=annualMean,
          cmap='inferno', alpha=0.75)

# Create colorbar and legend
plt.colorbar(label=r'${\rm sunshine}$', fraction=0.033, pad=0.04)

plt.title('Hours of Sunshine in Weather Stations of WMO')

plt.show()


# In[ ]:




