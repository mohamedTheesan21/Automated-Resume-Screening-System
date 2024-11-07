import pandas as pd
import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from test_utils import preprocess_data, idx2tag, predict_on_chunks
import re

MAX_LEN = 512
NUM_LABELS = 12
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = 'bert-base-uncased'
STATE_DICT = torch.load("model-state.bin", map_location=DEVICE)
TOKENIZER = BertTokenizerFast.from_pretrained(
    MODEL_PATH, do_lower_case=True, timeout=300)

model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased', state_dict=STATE_DICT['model_state_dict'], num_labels=NUM_LABELS)
model.to(DEVICE)


######################## code to get the pdfs here################################
def extract_entities(data, Name, input_skills):

    try:
        resume_text, References = preprocess_data(data)
        entities = predict_on_chunks(model, TOKENIZER, idx2tag,
                                     DEVICE, resume_text, MAX_LEN)

        # compare and update skills
        matched_skills = compare_and_update_skills([skill.strip()  # remove any leading/trailing whitespace
                                                    for entity in entities if entity['entity'] == 'Skills'
                                                    for skill in entity['text'].split(',')], input_skills)

        # Separate entities by category
        # Skills = ', '.join([entity['text'] for entity in entities if entity['entity'] == 'Skills'])
        Skills = ', '.join(matched_skills)
        # Education = ', '.join(
        #     [entity['text'] for entity in entities if entity['entity'] == 'Degree'])
        # Experience = ', '.join(
        #     [entity['text'] for entity in entities if entity['entity'] == 'Designation'])
        Education = ', '.join(
            [re.sub(r'[^\w\s]+', '', entity['text']) for entity in entities if entity['entity'] == 'Degree'])
        Experience = ', '.join(
            [re.sub(r'[^\w\s]+', '', entity['text']) for entity in entities if entity['entity'] == 'Designation'])

        resume_data_df = pd.DataFrame(
            columns=['Name', 'Skills', 'Education', 'Experience', 'References'])

        # Append to DataFrame
        resume_data_df.loc[len(resume_data_df)] = [
            Name, Skills, Education, Experience, References]

        return resume_data_df
    except Exception as e:
        print(e)
        return None

# Updated function to match extracted skills and update the skills array


def compare_and_update_skills(extracted_skills, input_skills):
    # Convert extracted skills and input skills to lowercase for consistency
    extracted_skills = [skill.lower() for skill in extracted_skills]
    input_skills = [skill.lower() for skill in input_skills]
    skills = [skill.lower() for skill in skills_array]

    # Add any missing skills from input_skills to the skills array
    for skill in input_skills:
        if skill not in skills:
            # Capitalize to match format
            skills_array.append(skill.capitalize())

    # Compare with the predefined skills array
    matched_skills = [
        skill for skill in skills_array if skill.lower() in extracted_skills]

    return matched_skills


skills_array = [
    "Python","C", "Java", "SQL", "Data Analysis", "Machine Learning","Teamwork" "Project Management", "Communication",
    "Teamwork", "Problem Solving", "Leadership", "React", "FastAPI", "Natural Language Processing",
    "Time Management", "Critical Thinking", "Adaptability", "HTML", "CSS", "JavaScript", "Cloud Computing",
    "DevOps", "Docker", "Kubernetes", "Git", "Version Control", "Agile Methodology", "Scrum",
    "Product Management", "Financial Analysis", "Accounting", "Salesforce", "Customer Relationship Management",
    "Business Intelligence", "Tableau", "Power BI", "Data Visualization", "Statistical Analysis",
    "Regression Analysis", "Artificial Intelligence", "Deep Learning", "Data Engineering", "ETL", "Big Data",
    "Apache Spark", "Hadoop", "Data Warehousing", "TensorFlow", "Keras", "PyTorch",
    "Natural Language Generation", "Speech Recognition", "Computer Vision", "AWS", "Azure", "Google Cloud Platform",
    "Linux", "Unix", "Network Security", "Cybersecurity", "Penetration Testing", "Information Security", "Blockchain",
    "Smart Contracts", "Digital Marketing", "SEO", "Content Marketing", "Copywriting", "Social Media Marketing",
    "Market Research", "Brand Strategy", "Customer Support", "Technical Support", "Business Strategy",
    "Strategic Planning", "Supply Chain Management", "Operations Management", "Logistics", "Negotiation",
    "Public Speaking", "Conflict Resolution", "Emotional Intelligence", "Cross-Functional Collaboration", "C++",
    "C#", "Objective-C", "Swift", "Mobile Development", "iOS Development", "Android Development",
    "Frontend Development", "Backend Development", "UI/UX Design", "Prototyping", "Wireframing",
    "Adobe Photoshop", "Adobe Illustrator", "Adobe XD", "Figma", "Canva", "Software Testing", "Unit Testing",
    "System Administration", "Customer Success", "Content Creation", "Database Management", "MongoDB", "MySQL",
    "PostgreSQL", "Oracle Database", "NoSQL", "Redis", "JIRA", "Confluence", "Trello", "Slack", "Microsoft Office",
    "Excel", "Word", "PowerPoint", "Google Analytics", "Google Ads", "Bing Ads", "Email Marketing", "HubSpot",
    "Marketo", "WordPress", "Shopify", "eCommerce", "Sales Strategy", "Lead Generation", "Cold Calling",
    "Sales Forecasting", "Customer Retention", "Client Relations", "Event Planning", "Talent Acquisition",
    "Recruiting", "Onboarding", "Performance Management", "Training and Development", "Compensation and Benefits",
    "Payroll Management", "Labor Law", "Employee Relations", "Diversity and Inclusion", "Risk Management",
    "Financial Modeling", "Budgeting", "Forecasting", "Investment Analysis", "Portfolio Management", "Mergers and Acquisitions",
    "Due Diligence", "Risk Assessment", "Compliance", "Audit", "Tax Planning", "Legal Writing", "Contract Management",
    "Intellectual Property", "Litigation", "Case Management", "Public Relations", "Media Relations",
    "Crisis Communication", "Brand Management", "Marketing Strategy", "Customer Insights", "Consumer Behavior",
    "Quantitative Analysis", "Qualitative Analysis", "Research Design", "Survey Design", "Data Cleaning",
    "Data Mining", "Predictive Modeling", "Data Integration", "Reporting", "SQL Server", "ETL Development",
    "Cloud Architecture", "Network Engineering", "System Design", "Infrastructure Management", "VPN",
    "Firewall Management", "Virtualization", "Vmware", "Hyper-V", "AWS Lambda", "Serverless Computing",
    "CI/CD Pipelines", "Automation", "Scripting", "Shell Scripting", "Bash", "PowerShell", "Ansible",
    "Chef", "Puppet", "Terraform", "Jenkins", "ElasticSearch", "Kafka", "RabbitMQ", "Microservices",
    "REST API", "GraphQL", "gRPC", "SOAP", "WebSockets", "Django", "Flask", "Node.js", "Express.js",
    "Angular", "Vue.js", "Bootstrap", "Tailwind CSS", "Sass", "Less", "Responsive Design", "Cross-Browser Compatibility",
    "User Research", "Usability Testing", "A/B Testing", "Heatmaps", "Wireframes", "Mockups", "Prototyping",
    "Storyboarding", "3D Modeling", "Game Development", "Unity", "Unreal Engine", "Augmented Reality",
    "Virtual Reality", "Robotics", "Automation Testing", "Selenium", "Cypress", "Manual Testing", "Performance Testing",
    "Load Testing", "Security Testing", "Penetration Testing", "Compliance Testing", "Quality Assurance",
    "Test Planning", "Bug Tracking", "Test Case Design", "Version Control", "Continuous Integration", "Continuous Delivery",
    "API Testing", "Mobile Testing", "Database Testing", "Integration Testing", "System Testing",
    "Acceptance Testing", "MATLAB", "Simulink", "LabVIEW", "Embedded Systems", "Control Systems",
    "Electrical Engineering", "Circuit Design", "PCB Design", "SolidWorks", "AutoCAD", "CATIA", "3D Printing",
    "Technical Writing", "Proposal Writing", "Grant Writing", "Creative Writing", "Editing", "Proofreading",
    "Research", "Market Analysis", "Competitor Analysis", "Innovation Management", "Design Thinking",
    "Lean Startup", "Customer Experience", "Customer Journey Mapping", "Behavioral Psychology"
]
