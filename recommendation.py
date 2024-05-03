#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import joblib
import pandas as pd

#create a function to scale student_input using same scaler used to scale the data

# student_input should look like this:
#     student_input = {
#     'sat_crit_read_75_pctl': 780,  # Example values
#     'sat_math_75_pctl': 790,
#     'tuition_fees_ft': 25000  # Example values
# }

def scale_student_input(student_input):
    scaler = joblib.load('scaler.joblib')
    
    # Assuming student_input is a dictionary, convert to DataFrame for scaling
    student_input_df = pd.DataFrame([student_input])
    
    # Scale the student inputs using the loaded scaler
    scaled_student_input = scaler.transform(student_input_df)
    scaled_student_input_df = pd.DataFrame(scaled_student_input, columns=student_input.keys(), )
    return scaled_student_input_df

#create a function that takes student_input and state and outputs a list of recommended institutions with their success scores

def recommend_institutions(student_input, state):
    # Load scaled dataset
    df_scaled = pd.read_csv('cleaned_df_in_state.csv')
    
    # Scale the student's input
    scaled_student_input = scale_student_input(student_input)
    #features
    features = ['sat_crit_read_75_pctl', 'sat_math_75_pctl', 'tuition_fees_ft']
    #distances
    distances = euclidean_distances(df_scaled[features], scaled_student_input)

    # Convert distances to similarity scores
    similarity_scores = np.exp(-distances)

    # Flatten the similarity scores array if necessary
    df_scaled['similarity_score'] = similarity_scores.flatten()

    #Filter by state
    df_scaled = df_scaled[df_scaled['state_abbr']==state]

    # Sort the DataFrame based on similarity scores
    recommended_institutions = df_scaled.sort_values(by='similarity_score', ascending=False)

    # Select the top ten institutions based on similarity score
    top_ten_institutions = recommended_institutions.head(10)

    # Sort these top ten institutions by the success_score column
    sorted_top_ten_by_success_score = top_ten_institutions.sort_values(by='success_score', ascending=False)
    
    # Convert to JSON (for web consumption)
    recommendations_json = sorted_top_ten_by_success_score[['inst_name','success_score']].to_json(orient='records')
    return recommendations_json


# In[2]:





# In[ ]:




