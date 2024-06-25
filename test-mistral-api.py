import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import pandas as pd
from mistralai.models.jobs import TrainingParameters
from datasets import load_dataset
from mistralai.models.chat_completion import ChatMessage
import time

# Manually set the environment variable
os.environ["MISTRAL_API_KEY"] = "8BXU9qP4ba24JS0OY7vS1kdRpRWFNvfT"

# Retrieve the API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]
client = MistralClient(api_key=api_key)

"""
with open("interview_training_data.jsonl", "rb") as f:
    training_data = client.files.create(file=("interview_training_data.jsonl", f))"""

with open("training_file.jsonl", "rb") as f:
    training_data = client.files.create(file=("training_file.jsonl", f))

with open("validation_file.jsonl", "rb") as f:
    validation_data = client.files.create(file=("validation_file.jsonl", f))
                                        
created_jobs = client.jobs.create(
    model="open-mistral-7b",
    training_files=[training_data.id],
    validation_files=[validation_data.id],
    hyperparameters=TrainingParameters(
        training_steps=10,
        learning_rate=0.0001,
        )
)

created_jobs


job_id = created_jobs.id
job_status = created_jobs.status

if hasattr(created_jobs, 'model_name'):
    fine_tuned_model_name = created_jobs.model_name
else:
    fine_tuned_model_name = None  # Handle case where model name is not available

# Retrieve a jobs
retrieved_job = client.jobs.retrieve(created_jobs.id)
print(retrieved_job)

#client.jobs.cancel(created_jobs.id)

job_id = created_jobs.id
job_status = ""
while job_status != "SUCCESS":
    retrieved_job = client.jobs.retrieve(job_id)
    job_status = retrieved_job.status
    print(f"Job status: {job_status}")
    if job_status == "RUNNING":
        time.sleep(60)  # Wait for 60 seconds before checking the status again

fine_tuned_model_name = retrieved_job.fine_tuned_model  # This might not be the correct way to access the fine-tuned model
chat_response = client.chat(
    model=fine_tuned_model_name,
    messages=[ChatMessage(role='user', content="Je m'appelle Eva")]
)
print(chat_response)
                                   