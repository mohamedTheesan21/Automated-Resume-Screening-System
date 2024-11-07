import torch
import numpy as np
from pdfminer.high_level import extract_text
import re

references_titles = [
    "References",
    "Professional References",
    "Personal References",
    "Work References",
    "Employment References",
    "References Available Upon Request",
    "Referees",
    "Recommendation Contacts",
    "Contactable References",
    "Reference List",
    "Professional Contacts",
    "Endorsements",
    "People Who Can Vouch for Me",
    "Relevant Contacts",
    "Credentials",
    "Recommendations",
    "Recommendations Upon Request",
    "Available Upon Request",
    "Supporting Contacts Provided on Request"
]

# def remove_below_references(text):
#     # Join the reference titles into a regex pattern (case insensitive)
#     pattern = '|'.join(re.escape(title) for title in references_titles)
    
#     # Find where any of the references section starts and truncate everything below it
#     match = re.search(pattern, text, re.IGNORECASE)
#     references = ""
#     if match:
#         # Keep text up to the start of the References section
#         references = text[match.start():]
#         text = text[:match.start()]

    
#     return text, references

def remove_below_references(text):
    references_titles = ['References', 'Referrals','Reference']  # Update as needed
    
    # Join the reference titles into a regex pattern (case insensitive)
    pattern = r'|'.join([r'\b' + re.escape(title) + r'\b' for title in references_titles])
    
    # Find where any of the references section starts and truncate everything below it
    match = re.search(pattern, text, re.IGNORECASE)
    references = ""
    if match:
        # Keep text up to the start of the References section
        references = text[match.start():]
        text = text[:match.start()]
    
    return text,references



def preprocess_data(data):
    text = extract_text(data)
    text = text.replace("\n", " ")
    text = text.replace("\f", " ")
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Replace pipe '|' with space
    text = text.replace("|", ",")
    text, references= remove_below_references(text)

    return text, references


def tokenize_resume(text, tokenizer, max_len):
    tok = tokenizer.encode_plus(
        text, max_length=max_len, return_offsets_mapping=True)

    curr_sent = dict()

    padding_length = max_len - len(tok['input_ids'])

    curr_sent['input_ids'] = tok['input_ids'] + ([0] * padding_length)
    curr_sent['token_type_ids'] = tok['token_type_ids'] + \
        ([0] * padding_length)
    curr_sent['attention_mask'] = tok['attention_mask'] + \
        ([0] * padding_length)

    final_data = {
        'input_ids': torch.tensor(curr_sent['input_ids'], dtype=torch.long),
        'token_type_ids': torch.tensor(curr_sent['token_type_ids'], dtype=torch.long),
        'attention_mask': torch.tensor(curr_sent['attention_mask'], dtype=torch.long),
        'offset_mapping': tok['offset_mapping']
    }

    return final_data


tags_vals = ["UNKNOWN", "O", "Name", "Degree", "Skills", "College Name", "Email Address",
             "Designation", "Companies worked at", "Graduation Year", "Years of Experience", "Location"]
idx2tag = {i: t for i, t in enumerate(tags_vals)}
resticted_lables = ["UNKNOWN", "O", "Email Address"]


# def predict(model, tokenizer, idx2tag, device, test_resume, max_len):
#     model.eval()
#     data = tokenize_resume(test_resume, tokenizer, max_len)
#     input_ids, input_mask = data['input_ids'].unsqueeze(
#         0), data['attention_mask'].unsqueeze(0)
#     labels = torch.tensor([1] * input_ids.size(0),
#                           dtype=torch.long).unsqueeze(0)

#     input_ids = input_ids.to(device)
#     input_mask = input_mask.to(device)
#     labels = labels.to(device)

#     with torch.no_grad():
#         outputs = model(
#             input_ids,
#             token_type_ids=None,
#             attention_mask=input_mask,
#             labels=labels,
#         )
#         tmp_eval_loss, logits = outputs[:2]

#     logits = logits.cpu().detach().numpy()
#     label_ids = np.argmax(logits, axis=2)

#     entities = []
#     for label_id, offset in zip(label_ids[0], data['offset_mapping']):
#         curr_id = idx2tag[label_id]
#         curr_start = offset[0]
#         curr_end = offset[1]
#         if curr_id not in resticted_lables:
#             if len(entities) > 0 and entities[-1]['entity'] == curr_id and curr_start - entities[-1]['end'] in [0, 1]:
#                 entities[-1]['end'] = curr_end
#             else:
#                 entities.append(
#                     {'entity': curr_id, 'start': curr_start, 'end': curr_end})
#     for ent in entities:
#         ent['text'] = test_resume[ent['start']:ent['end']]
    # return entities

def predict(model, tokenizer, idx2tag, device, test_resume, max_len):
    model.eval()
    data = tokenize_resume(test_resume, tokenizer, max_len)
    input_ids, input_mask = data['input_ids'].unsqueeze(0), data['attention_mask'].unsqueeze(0)
    
    # Updated labels to match the shape of input_ids
    labels = torch.ones(input_ids.size(), dtype=torch.long).to(device)

    input_ids = input_ids.to(device)
    input_mask = input_mask.to(device)

    with torch.no_grad():
        outputs = model(
            input_ids,
            token_type_ids=None,
            attention_mask=input_mask,
            labels=labels,
        )
        tmp_eval_loss, logits = outputs[:2]

    logits = logits.cpu().detach().numpy()
    label_ids = np.argmax(logits, axis=2)

    entities = []
    for label_id, offset in zip(label_ids[0], data['offset_mapping']):
        curr_id = idx2tag[label_id]
        curr_start = offset[0]
        curr_end = offset[1]
        if curr_id not in resticted_lables:
            if len(entities) > 0 and entities[-1]['entity'] == curr_id and curr_start - entities[-1]['end'] in [0, 1]:
                entities[-1]['end'] = curr_end
            else:
                entities.append(
                    {'entity': curr_id, 'start': curr_start, 'end': curr_end})
    for ent in entities:
        ent['text'] = test_resume[ent['start']:ent['end']]
    return entities

def predict_on_chunks(model, tokenizer, idx2tag, device, resume_text, max_len):
    entities = []
    for i in range(0, len(resume_text), max_len):
        entities.extend(predict(model, tokenizer, idx2tag, device, resume_text[i:i+max_len], max_len))
    return entities
