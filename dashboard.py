import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

df_final = pd.read_csv("./back-end/all_resumes_data.csv")
print("Dashboard Starting...")

# Set up the Streamlit app
st.set_page_config(page_title="ARSS", page_icon="📄", layout="wide")

st.title("Automated Resume Screening and Ranking System")

# Word Cloud Function
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

df_final['Skills'] = df_final['Skills'].astype(str)

# Split, explode, and convert to list
skills_list = df_final['Skills'].apply(lambda x: x.split(",")).explode().tolist()
print(type(skills_list))  # Should be <class 'list'>


with st.container():
    st.subheader("Your Screening Results")
    
    skills_text = ', '.join(skills_list)
    wordcloud = generate_wordcloud(skills_text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

col1,= st.columns(1)

# Skills Distribution
with col1:
    st.subheader("Skills Distribution")
    skills_count = pd.Series(skills_list).value_counts()
    # print(skills_count)
    fig = px.bar(x=skills_count.index, y=skills_count.values, labels={'x': 'Skill', 'y': 'Count'}, title="Skills Distribution")
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
    st.write(f"*Name:* {candidate_data['Name']}")
    st.write(f"*Skills:* {candidate_data['Skills']}")
    st.write(f"*Education:* {candidate_data['Education']}")
    st.write(f"*Experience:* {candidate_data['Experience']}")

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