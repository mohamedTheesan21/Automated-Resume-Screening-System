import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from test_utils import preprocess_data, idx2tag, predict_on_chunks

MAX_LEN = 512
NUM_LABELS = 12
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = 'bert-base-uncased'
STATE_DICT = torch.load("model-state.bin", map_location=DEVICE)
TOKENIZER = BertTokenizerFast.from_pretrained(MODEL_PATH, do_lower_case=True)

model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased', state_dict=STATE_DICT['model_state_dict'], num_labels=NUM_LABELS)
model.to(DEVICE)


########################code to get the pdfs here################################
# eg : 
data = ("C:/Users/DELL/Downloads/Disini Thevinka_210647C_Fortude.pdf")
resume_text, references = preprocess_data(data)
entities = predict_on_chunks(model, TOKENIZER, idx2tag,
                    DEVICE, resume_text, MAX_LEN)
print({'entities': entities})

skills = [entity['text'] for entity in entities if entity['entity'] == 'Skills']
joined_skills = ', '.join(skills)

print("\n\n\n\n\n\n\n\n\n")
print({'skills': joined_skills})


##in a loop read all the files and extract information to a dataframe



