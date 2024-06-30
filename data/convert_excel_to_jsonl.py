import pandas as pd
import json

# Read the Excel file into a DataFrame
excel_data_df = pd.read_excel('interview-dataset.xlsx')

# Initialize an empty list to store each conversation sample
conversation_samples = []

# Iterate over the rows of the DataFrame
#for index, row in excel_data_df.dropna().iterrows():
for index, row in excel_data_df.iterrows():
    # Create a conversation sample for each row    
    conversation = {
        "messages": [
            {"role": "assistant", "content": row["Question"]},
            {"role": "user", "content": row["Reponse"]},
            {"role": "assistant", "content": row["Feedback"]}
        ]
    }
   
    # Append the conversation sample to the list
    conversation_samples.append(conversation)



# Write the JSON string to a file
with open('interview_training_data.jsonl', 'w', encoding='utf-8') as outfile:
    for entry in conversation_samples:
        json.dump(entry, outfile)
        outfile.write('\n')

print('Data has been successfully converted and saved to interview_training_data.jsonl')
