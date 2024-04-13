# Meeting Transcript Summarization and Agenda Extraction

## Overview

This repository contains a Python AWS Lambda function that facilitates efficient summarization of meeting transcripts and extraction of key agenda items. The code leverages the following technologies and techniques:

- BeautifulSoup: For parsing HTML content within agenda items.
- LangChain: To streamline interaction with large language models and build powerful text processing chains.
- Bedrock LLM: A powerful language model from AI21 Labs (accessed via the Bedrock runtime client) is employed for text summarization.

## Functionality

- Agenda Extraction: Parses meeting data (JSON format) to extract agenda items and creates a clearly formatted agenda string.
- Transcript Processing: Splits the meeting transcript into manageable text chunks for downstream processing.
- Text Summarization: Utilizes a state-of-the-art LLM (Bedrock) through LangChain to intelligently summarize the meeting transcript.

## Prerequisites

- AWS account with permissions to create Lambda functions and S3 buckets.
- An API key or access credentials to use the Bedrock LLM (if you choose this LLM).

## Usage

1. Clone this repository.
2. Create an AWS Lambda function and upload the provided code.
3. Configure an S3 trigger to invoke the Lambda function whenever a meeting transcript JSON file is uploaded to a designated bucket.
4. The summarized text and the extracted agenda will be available in a designated destination S3 bucket.

## Customization

- Experiment with other LLMs supported by LangChain for text summarization.
- Modify agenda formatting as needed.

## Example Input (JSON)

```json
{
  "transcript": "Long meeting transcript text...",
  "agenda_items": [
    {
      "item_number": 1,
      "content": "<p>Discussion of project status</p>"
    }
  ]
}
