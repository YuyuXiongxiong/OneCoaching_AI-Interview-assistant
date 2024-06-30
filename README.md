# OneCoaching AI Interview Assistant

## Description

OneCoaching AI Interview Assistant is designed to help students prepare for interviews by:
- Generating random interview questions tailored to specific sectors.
- Allowing real-time practice sessions.
- Providing feedback and improved versions of responses.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Fine Tuning](#fine-tuning)
- [Contact](#contact)

## Installation

Follow these steps to set up the development environment:

```bash
# Clone the repository
git clone https://github.com/YuyuXiongxiong/OneCoaching_AI-Interview-assistant.git

# Navigate to the project directory
cd OneCoaching_AI-Interview-assistant
```

## Usage

Instructions on how to use the project. Include code snippets and examples if necessary.

```bash
# Start the application
chainlit run app.py
```

## Fine Tuning

The model is fine-tuned using the `interview_training_data.jsonl` file. If you want to create your own training data, follow these steps:

1. Create an Excel file with the format `interview-dataset.xlsx`.

2. Convert the Excel file to JSONL format:

    ```bash
    # Run the conversion script
    python convert_excel_to_jsonl.py
    ```

3. Reformat the data:

    ```bash
    # Run the reformatting script
    python reformat_data.py interview_training_data.jsonl
    ```

4. Fine-tune the model:

    ```bash
    # Run the fine-tuning script
    python finetune.py
    ```

## Contact

For any questions or inquiries, please contact:

- **Eva XI**
- **Email:** xyq824@gmail.com
