Link del dataset: https://archive.ics.uci.edu/dataset/73/mushroom
Explicación de los campos:


poisonous	                Target	Categorical			
cap-shape	                Feature	Categorical	bell=b, conical=c, convex=x, flat=f, knobbed=k, sunken=s		
cap-surface	                Feature	Categorical	fibrous=f, grooves=g, scaly=y, smooth=s		
cap-color	                Feature	Binary	    brown=n, buff=b, cinnamon=c, gray=g, green=r, pink=p, purple=u, red=e, white=w, yellow=y		
bruises	                    Feature	Categorical	bruises=t,no=f		
odor	                    Feature	Categorical	almond=a,anise=l,creosote=c,fishy=y,foul=f, musty=m,none=n,pungent=p,spicy=s		
gill-attachment	            Feature	Categorical	attached=a,descending=d,free=f,notched=n		
gill-spacing	            Feature	Categorical	close=c,crowded=w,distant=d		
gill-size	                Feature	Categorical	broad=b,narrow=n		
gill-color	                Feature	Categorical	black=k,brown=n,buff=b,chocolate=h,gray=g, green=r,orange=o,pink=p,purple=u,red=e, white=w,yellow=y		
stalk-shape	                Feature	Categorical	enlarging=e,tapering=t		
stalk-root	                Feature	Categorical	bulbous=b,club=c,cup=u,equal=e, rhizomorphs=z,rooted=r,missing=?		
stalk-surface-above-ring	Feature	Categorical	fibrous=f,scaly=y,silky=k,smooth=s		
stalk-surface-below-ring	Feature	Categorical	fibrous=f,scaly=y,silky=k,smooth=s		
stalk-color-above-ring	    Feature	Categorical	brown=n,buff=b,cinnamon=c,gray=g,orange=o, pink=p,red=e,white=w,yellow=y		
stalk-color-below-ring	    Feature	Categorical	brown=n,buff=b,cinnamon=c,gray=g,orange=o, pink=p,red=e,white=w,yellow=y		
veil-type	                Feature	Binary	    partial=p,universal=u		
veil-color	                Feature	Categorical	brown=n,orange=o,white=w,yellow=y		
ring-number	                Feature	Categorical	none=n,one=o,two=t		
ring-type	                Feature	Categorical	cobwebby=c,evanescent=e,flaring=f,large=l, none=n,pendant=p,sheathing=s,zone=z		
spore-print-color	        Feature	Categorical	black=k,brown=n,buff=b,chocolate=h,green=r, orange=o,purple=u,white=w,yellow=y		
population	                Feature	Categorical	abundant=a,clustered=c,numerous=n, scattered=s,several=v,solitary=y		
habitat	                    Feature	Categorical	grasses=g,leaves=l,meadows=m,paths=p, urban=u,waste=w,woods=d		



import pandas as pd

# Nombres oficiales de las 23 columnas (UCI agaricus-lepiota.names)
# La primera columna es el TARGET: e=edible, p=poisonous
columnas = [
    'class',                      # TARGET
    'cap_shape', 'cap_surface', 'cap_color',
    'bruises', 'odor',
    'gill_attachment', 'gill_spacing', 'gill_size', 'gill_color',
    'stalk_shape', 'stalk_root',
    'stalk_surface_above_ring', 'stalk_surface_below_ring',
    'stalk_color_above_ring', 'stalk_color_below_ring',
    'veil_type', 'veil_color',
    'ring_number', 'ring_type',
    'spore_print_color', 'population', 'habitat'
]

df = pd.read_csv(
    'agaricus-lepiota.data',
    header=None,
    names=columnas,
    na_values='?'   # los '?' (en stalk_root) se convierten en NaN reales
)

df.to_csv('mushroom.csv', index=False)
print("CSV creado:", df.shape)
print(df.head())
print("\nNulos por columna:")
print(df.isnull().sum()[df.isnull().sum() > 0])
print("\nBalance del target:")
print(df['class'].value_counts(normalize=True).round(3))
