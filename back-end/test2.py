import io
import torch
from transformers import BertTokenizerFast, BertForTokenClassification
from flask import Flask, jsonify, request
from server.utils import preprocess_data, idx2tag, predict_on_chunks

MAX_LEN = 512
NUM_LABELS = 12
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = 'bert-base-uncased'
STATE_DICT = torch.load("model-state.bin", map_location=DEVICE)
TOKENIZER = BertTokenizerFast("./vocab/vocab.txt", lowercase=True)

model = BertForTokenClassification.from_pretrained(
    'bert-base-uncased', state_dict=STATE_DICT['model_state_dict'], num_labels=NUM_LABELS)
model.to(DEVICE)


# @app.route('/predict', methods=['POST'])
# def predict_api():
#     if request.method == 'POST':
data = ("demo/Resume - Ayush Srivastava.pdf")
resume_text, references = preprocess_data(data)
entities = predict_on_chunks(model, TOKENIZER, idx2tag,
                    DEVICE, resume_text, MAX_LEN)
print({'entities': entities})

skills = [entity['text'] for entity in entities if entity['entity'] == 'Skills']
joined_skills = ', '.join(skills)

print("\n\n\n\n\n\n\n\n\n")
print({'skills': joined_skills})
