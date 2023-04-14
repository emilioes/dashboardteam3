# Covid-19 Dashboard


## Collaborators
- Romaric Sallustre
- Alexis Culpin
- Emilio Espinosa 


## Objective
To provide an open-source project interactive Covid-19 dashboard that allows users to visualize the number of Covid-19 cases or deaths per country as a function of time.


## Introduction
Dashboard is an essential component of data science. It offers a visual and interactive way to explore data. It is often built upon web-based technologies.
During the Covid-19 pandemic, many dashboards were created to allow citizens to follow the evolution of the outbreak. One of the most popular, whose graphics have often been used in the news, is that of Our World in Data

## Data source
The data use for this project was obtained from the following Github repository <a href="https://github.com/owid/covid-19-data" target="_new">Covid-19 data</a>.

## Requirements
- Python 3.8 or above.
- Pandas.
- Matplotlib.
- <a href="https://streamlit.io/">Streamlit</a>. 
- Numpy.
- Plotly Express.
Once you created your environement (see following step), you can install all Requirements with the following command :
```
python -m pip install -r requirements.txt
```

# Installation guidelines

## For windows :
For windows users the step to create an environment are the following:

##### 1. Open the command prompt.
Press your start button and type "cmd".
Alternativelly Shift + right click on the folder you want and click on "open a command prompt here".

##### 2. Clone the repository in the desired folder with the following command:
```
git clone https://github.com/emilioes/dashboardteam3.git
```
##### 3. Go into the created  folder :
```
cd dashboardteam3
```
Then, to  create an environment run :
```
python -m venv env
```

##### 4. To activate the environment run :
```
env\Scripts\activate
```
##### 5. To install the requiered package  for this project run :
```
python -m pip install -r requirements.txt
```
##### Additional: If you want  to close the environment run : 
```
deactivate
```

## For unix (and wsl):
For unix users the step to create an environment are the following:

##### 1. Open the command prompt.

##### 2. Clone the repository in the desired folder with the following command:
```
git clone https://github.com/emilioes/dashboardteam3.git
```
##### 3. Go into the created  folder :
```
cd dashboardteam3
```
Then, to  create an environment run :
```
python -m venv env
```

##### 4. To activate the environment run :
```
source env/bin/activate
```
##### 5. To install the requiered package  for this project run :
```
python -m pip install -r requirements.txt
```
##### Additional: If you want  to close the environment run : 
```
deactivate
```


## Instructions
If you want to run the dashboard on your local machine, (for testing and debuging mainly), it's quite easy !
Make sure you created and activated your environment with the step above.
Once it's done simply run :
```
streamlit run script/dashBoard.py
```
Let it run, your browser should open a new page with your dashboard.
If not, check your command prompt the link to your local dashboard will be printed, just copy it and past it to your browser.

## Streamlit Cloud Integration
The URL of the COVID-19 dashboard is given here: <a href="http://localhost:8501/">LOCAL URL</a>

## Contribution
Feel free to fork the project, and make changes and pull request.

## License
This project is under <a href="https://github.com/emilioes/dashboardteam3/blob/main/LICENSE" target="_new">MIT</a> licence.

[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:3e7f303437d4f680dbd09990cf3d630947a2e487/)][def]

[def]: https://archive.softwareheritage.org/swh:1:dir:3e7f303437d4f680dbd09990cf3d630947a2e487;origin=https://github.com/emilioes/dashboardteam3;visit=swh:1:snp:9a5b141fcd7dd386ca7167f86ccae6b014492187;anchor=swh:1:rev:83024e76fa1e2282e51c22622ac23f947b26a51c