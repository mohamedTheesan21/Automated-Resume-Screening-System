import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from test_utils import preprocess_data, idx2tag, predict_on_chunks

MAX_LEN = 512
NUM_LABELS = 12
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = 'bert-base-uncased'
STATE_DICT = torch.load("model-state.bin", map_location=DEVICE)
TOKENIZER = BertTokenizerFast.from_pretrained(MODEL_PATH, do_lower_case=True, timeout=300)

model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased', state_dict=STATE_DICT['model_state_dict'], num_labels=NUM_LABELS)
model.to(DEVICE)


########################code to get the pdfs here################################
def extract_entities(data):
    
    resume_text, references = preprocess_data(data)
    entities = predict_on_chunks(model, TOKENIZER, idx2tag,
                    DEVICE, resume_text, MAX_LEN)
    print({'entities': entities})

    skills = [entity['text'] for entity in entities if entity['entity'] == 'Skills']
    joined_skills = ', '.join(skills)
    education = [entity['text'] for entity in entities if entity['entity'] == 'Education']
    joined_education = ', '.join(education)
    experience = [entity['text'] for entity in entities if entity['entity'] == 'Experience']
    joined_experience = ', '.join(experience)

    print("\n\n\n\n\n\n\n\n\n")
    print({'skills': joined_skills})
    print({'education': joined_education})
    print({'experience': joined_experience})

# score part have to do here

##in a loop read all the files and extract information to a dataframe