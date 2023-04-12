import streamlit as st
import pandas as pd
import numpy as np
from pulp import *

num_classes = st.slider('Number of Classes', min_value=1, max_value=10)
class_times = st.multiselect('Class Times', ['9:00am-10:30am', '10:45am-12:15pm', '1:00pm-2:30pm', '2:45pm-4:15pm', '4:30pm-6:00pm'], default=['9:00am-10:30am', '10:45am-12:15pm'])
class_days = st.multiselect('Class Days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], default=['Monday', 'Wednesday', 'Friday'])
num_students = st.number_input('Number of Students', min_value=1, max_value=1000, value=30)

# Define the optimization problem
model = LpProblem("Optimum Timetable", LpMinimize)

# Define the decision variables
days = class_days
times = class_times
variables = LpVariable.dicts("Class", [(d,t) for d in days for t in times], cat='Binary')

# Define the objective function
model += lpSum([variables[(d,t)] for d in days for t in times])

# Define the constraints
for d in days:
    model += lpSum([variables[(d,t)] for t in times]) == num_classes
for t in times:
    model += lpSum([variables[(d,t)] for d in days]) <= 1

# Solve the optimization problem
model.solve()

# Output the results
st.write('Optimum Timetable:')
for d in days:
    st.write(d)
    for t in times:
        if variables[(d,t)].value() == 1.0:
            st.write(t)
