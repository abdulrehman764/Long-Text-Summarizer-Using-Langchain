import json
import boto3
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.bedrock import Bedrock
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import time

def extract_agenda_items(data):
    extracted_data = []
    try:
        for item in data['agenda_items']:
            soup = BeautifulSoup(item['content'], 'html.parser')
            text = soup.get_text(separator='/n', strip=True)
            extracted_data.append({'item_number': item['item_number'], 'text': text})
    except:
        print("No agenda items found")
    return extracted_data

def generate_agenda_string(extracted_data):
    Agenda = [item['text'] for item in extracted_data]
    agenda_string = "Meeting Agenda: \n"
    for j, item_text in enumerate(Agenda):
        agenda_string += f"{j+1}. {item_text} \n"
    return agenda_string

def process_transcript(data):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "."], chunk_size=15000, chunk_overlap=3000
    )
    docs = text_splitter.create_documents([data['transcript']])
    return docs

def initialize_bedrock():
    boto3_bedrock = boto3.client(service_name='bedrock-runtime')
    modelId = "ai21.j2-ultra-v1"
    llm = Bedrock(
        model_id=modelId,
        model_kwargs={
            "maxTokens": 8191,
            "stopSequences": [],
            "temperature": 0,
            "topP": 1
        },
        client=boto3_bedrock,
    )
    return llm

def summarize_text(llm, docs):
    map_prompt = """
    Write a detailed summary of the following:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
    combine_prompt = """
    Write a detailed summary of the following text delimited by triple backquotes.
    Return your response which covers all the key points of the text.
    ```{text}```
    SUMMARY:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])
    summary_chain = load_summarize_chain(llm=llm, chain_type="map_reduce", verbose=True, return_intermediate_steps=True, map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template)
    output = summary_chain.invoke(docs)
    return output

def lambda_handler(event, context):
    # s3 = boto3.client('s3')
    
    # # Download the JSON file from the source S3 bucket
    # # Get source data from S3  
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = event['Records'][0]['s3']['object']['key']

    
    # # Read JSON file
    # json_object = s3.get_object(Bucket=bucket, Key=key)
    # data = json.load(json_object['Body'])

    with open('prs_meeting_20240208_api_request.json', 'r') as json_file:
        data = json.load(json_file)
    
    # Extract agenda items
    try:
        extracted_data = extract_agenda_items(data)
    except:
        print("No agenda found")
    
    # Generate agenda string
    try:
        agenda_string = generate_agenda_string(extracted_data)
    except:
        print("No agenda found")
    
    # Process transcript
    docs = process_transcript(data)
    
    # Initialize Bedrock
    llm = initialize_bedrock()
    
    # Summarize text
    s_time = time.time()
    output = summarize_text(llm, docs)
    e_time = time.time()
    print("Time: ", e_time - s_time)
    
    # Upload summary to the destination S3 bucket
    # s3.put_object(Body=output['output_text'], Bucket='summary-bucket', Key='summary.txt')
    print("Output: ", output['output_text'])
    return {
        'statusCode': 200,
        'body': json.dumps('Summary generated and uploaded successfully!')
    }


