import pandas as pd
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
def extract_entities(data, Name):

    try :
        resume_text, References = preprocess_data(data)
        entities = predict_on_chunks(model, TOKENIZER, idx2tag,
                        DEVICE, resume_text, MAX_LEN)
        
        # Separate entities by category
        Skills = ', '.join([entity['text'] for entity in entities if entity['entity'] == 'Skills'])
        Education = ', '.join([entity['text'] for entity in entities if entity['entity'] == 'Degree'])
        Experience = ', '.join([entity['text'] for entity in entities if entity['entity'] == 'Designation'])

        resume_data_df = pd.DataFrame(columns=['Name', 'Skills', 'Education', 'Experience', 'References'])

        # Append to DataFrame
        resume_data_df.loc[len(resume_data_df)] = [Name, Skills, Education, Experience, References]
        
        return resume_data_df
    except Exception as e:
        print(e)
        return None