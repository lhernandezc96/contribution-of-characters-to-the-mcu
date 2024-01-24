from bs4 import BeautifulSoup as bs
import requests
from collections import OrderedDict
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as py
import plotly.express as px
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots


url = 'https://www.imdb.com/list/ls507232408/?sort=release_date,asc&st_dt=&mode=detail&page=1'
page_source = requests.get(url)
soup = bs(page_source.content, 'lxml')
movies = []
movie_characters = []
movie_lengths = OrderedDict()
movies_dont_want = ["¿Qué pasaría si...?",
					 "Marvel de un vistazo: El consultor",
					"El caso único de Marvel: Algo divertido ocurrió de camino al martillo de Thor",
					"Marvel extendido: Artículo 47",
					"Todos aclaman al rey"]
for movie in soup.find_all('div', class_='lister-item mode-detail'):
		# Fetching title of the movie
		movie_title = movie.find('div', class_='lister-item-content').h3.a.text
		if movie_title in movies_dont_want:
			continue
		# Fetching length of the movie
		movie_length = movie.find('div', class_='lister-item-content').find('span', class_='runtime').text
		movies.append(movie_title)
		movie_lengths[movie_title] = movie_length.split(' ')[0]
		# Fetching characters in the movie
		characters = movie.find('div', class_='list-description').p.text
		movie_characters.append(characters.split('\n'))
data_dict = OrderedDict()
# Inputing data into the dictionary
for i in range(len(movies)):
	data_dict[movies[i]] = movie_characters[i]
data_dict['Loki'][0] = data_dict['Loki'][0].split('>')[1]+'>'
character_movie_time = {}
# Parsing through data scraped for each movie
for movie in data_dict.keys():
	# Parsing through each character in in the movie
	for item in data_dict[movie]:
		character = item.split('<')[0].strip()
		time = item.split('<')[1].split('>')[0].strip()
		# Adding time for each character to for each movie to the index dict
		if movie in character_movie_time.keys():
			character_movie_time[movie][character] = time
		else:
			character_movie_time[movie] = {character: time}
character_movie_time['Spider-Man: Homecoming']
char_id_index = pd.read_csv("src/data/characters.csv")
# Creating aa dict containing character IDs for each character
names = {old:new for (old, new) in zip(char_id_index['Character Name'], char_id_index['Character ID'])}
# Converting the data dict into a pandas data frame for easy handling
char_movie_matrix = pd.DataFrame(character_movie_time)

# Renaming characters with their character IDs
char_movie_matrix.rename(index=names, inplace=True)

def combine_rows(matrix):
	"""Method that combines the duplicate rows that arose due to replacing character IDs"""
	# List of characters
	characters = list(set([character for character in matrix.index]))
	# Iterating over every character
	for character in characters:
		# Creating a mini data frame for each character
		df = matrix.loc[character]
		# If the character row is present just once, iterating over every column would be iterating over every movie
		if len(list(df.index)) != len(matrix.columns):
			# Iterating over every movie for each character
			for movie in matrix.columns:
				# Initializing update value to NaN
				value = np.nan
				li = []
				# Creating a list of values for each movie
				for i in range(len(df.index)):
					li.append(str(df.iloc[i][movie]))
				# Updating the right value
				for item in li:
					if str(item) != 'nan':
						value = item
				# Updating value to the location
				matrix.loc[character, movie] = value
	# If there are n duplicates, n rows would have been created with same values; deleting the duplicates
	matrix = matrix.drop_duplicates()
	return matrix
# Combine rows with same index
char_movie_matrix = combine_rows(char_movie_matrix)
def convert_time_to_mins(matrix):
	"""Method that converts time of the format mm:ss or :ss or mm to minutes in float"""
	# Iterating over each character
	for character in matrix.index:
		# Iterating over each movie
		for movie in matrix.columns:
			# Current value of the cell in the matrix
			value = matrix.loc[character][movie]
			# Iterating over non NaN values only
			if str(value) != 'nan':
				# To convert strings of the format mm:ss
				if re.match(r'\d+:\d+', value):
					matrix.loc[character][movie] = float(value.split(':')[0]) + float(value.split(':')[1])/60
				# To convert strings of the format :ss
				elif re.match(r'^:\d+', value):
					matrix.loc[character][movie] = float(value.split(':')[1])/60
				# To convert strings of the format mm
				elif re.match(r'\b\d+\b(?!:)', value):
					matrix.loc[character][movie] = float(value)
				# Other formats assigned as NaN
				else:
					matrix.loc[character][movie] = np.nan
			# NaN values reassigned as NaN
			else:
				matrix.loc[character][movie] = np.nan
	return matrix
char_movie_matrix = convert_time_to_mins(char_movie_matrix)


char_movie_matrix = char_movie_matrix.fillna(0)


nueva_fila = pd.Series([False] * len(char_movie_matrix.columns), index=char_movie_matrix.columns, name='Serie')

for pelicula, duracion in movie_lengths.items():
    char_movie_matrix.loc['Serie', pelicula] = float(duracion) > 200
	
nueva_fila = pd.Series([0] * len(char_movie_matrix.columns), index=char_movie_matrix.columns, name='Fase')


for i in char_movie_matrix.columns:
    if i in char_movie_matrix.loc[:,'Iron Man':'Los Vengadores'].columns:
        char_movie_matrix.loc['Fase', i] = 1
    elif i in char_movie_matrix.loc[:,'Los Vengadores':'Ant-Man'].columns:
        char_movie_matrix.loc['Fase', i] = 2
    elif i in char_movie_matrix.loc[:,'Capitán América: Civil War':'Spider-Man: Lejos de casa'].columns:
        char_movie_matrix.loc['Fase', i] = 3
    elif i in char_movie_matrix.loc[:,'Bruja Escarlata y Visión' :'Guardianes de la Galaxia: Especial felices fiestas'].columns:
        char_movie_matrix.loc['Fase', i] = 4
    else:
        char_movie_matrix.loc['Fase', i] = 0

print(char_movie_matrix['Doctor Strange en el multiverso de la locura']['Scarlett Witch'])