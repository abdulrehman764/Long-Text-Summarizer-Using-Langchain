# Meeting Summarizer Lambda

This Lambda function extracts agenda items and generates a summary for meeting transcripts.

## Description

This Lambda function is designed to be triggered by events such as the upload of meeting data to an S3 bucket. It extracts agenda items from JSON data, processes meeting transcripts, and generates a detailed summary using language generation models provided by the Bedrock API.

## Features

- Extracts agenda items from JSON data
- Processes meeting transcripts
- Generates a detailed summary using language generation models
- Uploads the summary to an S3 bucket

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies as lambda layers using https://github.com/abdulrehman764/Lambda-Layer-Generator.
3. Set up your AWS credentials for Boto3.

## Usage

1. Ensure that your meeting data is in the correct format and stored in an S3 bucket.
2. Trigger the Lambda function manually or by configuring an event source, such as an S3 bucket upload event.

## Configuration

- Ensure that your AWS credentials are correctly configured.
- Modify the `lambda_handler` function to handle different types of events or customize the processing logic as needed.
- Adjust the parameters of the language generation models according to your requirements.

