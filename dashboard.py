<<<<<<< HEAD
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.patches as patches
import plotly.express as px
from wordcloud import WordCloud
import random

#simulation
def simulate():
    batch_size = 100  # Define batch size
    data_batch = []
    n_inputs = 50 #Take this from the inputs
    skills_list = ['Python', 'ML', 'Data Analysis', 'Java', 'SQL', 'Statistics', 'Data Visualization', 'Machine Learning', 'Deep Learning', 'R', 'Data Mining', 'Natural Language Processing', 'Big Data', 'Cloud Computing', 'Web Development', 'Git', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Tableau']
    education_levels = ['diploma', 'BSc', 'MSc', 'PHd']
    df_final = pd.DataFrame()
    for i in range(n_inputs):  # Assume 1000 resumes
        # Simulate extracted data (replace this with actual extraction logic)
        name = f'Person {i}'
        skills = random.sample(skills_list, random.randint(2, 6))
        education = random.choice(education_levels)
        experience = random.randint(0, 20)
        score = len(skills)*0.2 + (experience/10)*0.3  + (i+436)/23 # Simple scoring logic

        # Add data to the batch
        data_batch.append({
            'Name': name,
            'Skills': skills,
            'Education': education,
            'Experience': experience,
            'Score': score
        })

        # If batch is filled, process it
        if (i + 1) % batch_size == 0 or i == 49:  # Last batch
            df_batch = pd.DataFrame(data_batch)
            df_final = pd.concat([df_final, df_batch], ignore_index=True)
            data_batch = []  # Clear batch for next set

    # print(df_final.head())
    return df_final

df_final = simulate()
print("Dashboard Starting...")

# Set up the Streamlit app
st.set_page_config(page_title="ARSS", page_icon="📄", layout="wide")

st.title("Automated Resume Screening and Ranking System")

# Word Cloud Function
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Display Word Cloud for Skills in the first column

with st.container():
    st.subheader("Word Cloud - Skills")
    skills_text = ', '.join(df_final['Skills'].explode())
    wordcloud = generate_wordcloud(skills_text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    st.pyplot(fig)

col1, col2, col3 = st.columns(3)

# Skills Distribution
with col1:
    st.subheader("Skills Distribution")
    skills_count = df_final['Skills'].explode().value_counts()
    # print(skills_count)
    fig = px.bar(x=skills_count.index, y=skills_count.values, labels={'x': 'Skill', 'y': 'Count'}, title="Skills Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Education Level Distribution
with col2:
    st.subheader("Education Level Distribution")
    education_distribution = df_final['Education'].value_counts()
    fig = px.pie(education_distribution, names=education_distribution.index, values=education_distribution.values, title="Education Levels")
    st.plotly_chart(fig, use_container_width=True)

# Experience Distribution in the fourth column
with col3:
    st.subheader("Experience Distribution")
    fig = px.histogram(df_final, x='Experience', nbins=20, title="Experience in Years")
    st.plotly_chart(fig, use_container_width=True)

# Create a new row of columns for the next components

# Top Ranked Resumes in the first column
st.subheader("Top Ranked Resumes")
st.table(df_final[['Name', 'Score', 'Skills', 'Education', 'Experience']].sort_values(by='Score', ascending=False).head(5))

col1, col2 = st.columns(2)
# Candidate Overview in the third column
with col1:
    st.subheader("Candidate Overview")
    selected_candidate = st.selectbox("Select a candidate to view details", df_final['Name'])
    candidate_data = df_final[df_final['Name'] == selected_candidate].iloc[0]
    st.write(f"**Name:** {candidate_data['Name']}")
    st.write(f"**Skills:** {candidate_data['Skills']}")
    st.write(f"**Education:** {candidate_data['Education']}")
    st.write(f"**Experience:** {candidate_data['Experience']} years")

with col2:
    st.subheader("Download Results")
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df_final)
    st.download_button(
        "Download Ranked Resumes as CSV",
        data=csv,
        file_name='ranked_resumes.csv',
        mime='text/csv',
        help="centered"
    )
=======
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.patches as patches
import plotly.express as px
from wordcloud import WordCloud
import random

#simulation
def simulate():
    batch_size = 100  # Define batch size
    data_batch = []
    n_inputs = 50 #Take this from the inputs
    skills_list = ['Python', 'ML', 'Data Analysis', 'Java', 'SQL', 'Statistics', 'Data Visualization', 'Machine Learning', 'Deep Learning', 'R', 'Data Mining', 'Natural Language Processing', 'Big Data', 'Cloud Computing', 'Web Development', 'Git', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Tableau']
    education_levels = ['diploma', 'BSc', 'MSc', 'PHd']
    df_final = pd.DataFrame()
    for i in range(n_inputs):  # Assume 1000 resumes
        # Simulate extracted data (replace this with actual extraction logic)
        name = f'Person {i}'
        skills = random.sample(skills_list, random.randint(2, 6))
        education = random.choice(education_levels)
        experience = random.randint(0, 20)
        score = len(skills)*0.2 + (experience/10)*0.3  + (i+436)/23 # Simple scoring logic

        # Add data to the batch
        data_batch.append({
            'Name': name,
            'Skills': skills,
            'Education': education,
            'Experience': experience,
            'Score': score
        })

        # If batch is filled, process it
        if (i + 1) % batch_size == 0 or i == 49:  # Last batch
            df_batch = pd.DataFrame(data_batch)
            df_final = pd.concat([df_final, df_batch], ignore_index=True)
            data_batch = []  # Clear batch for next set

    # print(df_final.head())
    return df_final

df_final = simulate()
print("Dashboard Starting...")

# Set up the Streamlit app
st.set_page_config(page_title="ARSS", page_icon="📄", layout="wide")

st.title("Automated Resume Screening and Ranking System")

# Word Cloud Function
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Display Word Cloud for Skills in the first column

with st.container():
    st.subheader("Word Cloud - Skills")
    skills_text = ', '.join(df_final['Skills'].explode())
    wordcloud = generate_wordcloud(skills_text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    st.pyplot(fig)

col1, col2, col3 = st.columns(3)

# Skills Distribution
with col1:
    st.subheader("Skills Distribution")
    skills_count = df_final['Skills'].explode().value_counts()
    # print(skills_count)
    fig = px.bar(x=skills_count.index, y=skills_count.values, labels={'x': 'Skill', 'y': 'Count'}, title="Skills Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Education Level Distribution
with col2:
    st.subheader("Education Level Distribution")
    education_distribution = df_final['Education'].value_counts()
    fig = px.pie(education_distribution, names=education_distribution.index, values=education_distribution.values, title="Education Levels")
    st.plotly_chart(fig, use_container_width=True)

# Experience Distribution in the fourth column
with col3:
    st.subheader("Experience Distribution")
    fig = px.histogram(df_final, x='Experience', nbins=20, title="Experience in Years")
    st.plotly_chart(fig, use_container_width=True)

# Create a new row of columns for the next components

# Top Ranked Resumes in the first column
st.subheader("Top Ranked Resumes")
st.table(df_final[['Name', 'Score', 'Skills', 'Education', 'Experience']].sort_values(by='Score', ascending=False).head(5))

col1, col2 = st.columns(2)
# Candidate Overview in the third column
with col1:
    st.subheader("Candidate Overview")
    selected_candidate = st.selectbox("Select a candidate to view details", df_final['Name'])
    candidate_data = df_final[df_final['Name'] == selected_candidate].iloc[0]
    st.write(f"**Name:** {candidate_data['Name']}")
    st.write(f"**Skills:** {candidate_data['Skills']}")
    st.write(f"**Education:** {candidate_data['Education']}")
    st.write(f"**Experience:** {candidate_data['Experience']} years")

with col2:
    st.subheader("Download Results")
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df_final)
    st.download_button(
        "Download Ranked Resumes as CSV",
        data=csv,
        file_name='ranked_resumes.csv',
        mime='text/csv',
        help="centered"
    )
>>>>>>> 003365e13f945729d21c78d2b5ee88ec9e4e4843
