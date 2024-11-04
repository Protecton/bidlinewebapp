import os
import pypdf
import docx
import psycopg2
import weaviate
from ..services.supabase_service import init_supabase
from ..weaviate_client import weaviate_connection
from psycopg2 import sql

def extract_text_from_pdf(file):
    text = ''
    reader = pypdf.PdfReader(file)  # Replace PyPDF2.PdfReader with pypdf.PdfReader
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

# Function to extract text from Word document
def extract_text_from_word(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

# Function to slice text into smaller chunks
def slice_text(text, chunk_size=500):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def save_to_supabase(slices, rfp_id, user_id, proposal_id, company_id):
    try:
        # Initialize the Supabase client
        supabase = init_supabase()

        # Concatenate all slices into a single string
        concatenated_text = ' '.join(slices)

        # Insert the concatenated text into the request_for_proposals table
        data = {
            "id": rfp_id,
            "user_id": user_id,
            "proposal_id": proposal_id,
            "company_id": company_id,
            "description": concatenated_text}
        
        response = supabase.table('requests_for_proposals').upsert(data, on_conflict=['id']).execute()

        # Check for errors
        if response.data is None:
            raise Exception(f"Error saving to Supabase: {response}")
        
        return response
            
    except Exception as e:
        raise Exception(f"An error occurred while saving to Supabase: {e}")


def save_to_weaviate(slices, rfp_id, proposal_id, user_id, company_id):
    try:
        client = weaviate_connection()

        rfp_id = int(rfp_id)
        proposal_id = int(proposal_id)
        user_id = int(user_id)
        company_id = int(company_id)

        for index, slice_ in enumerate(slices):
            chunk_number = index + 1  # Set chunk number

            # Query for an object matching rfp_id, proposal_id, and chunk_number
            where_filter = {
                "operator": "And",
                "operands": [
                    {"path": ["rfp_id"], "operator": "Equal", "valueInt": rfp_id},
                    {"path": ["proposal_id"], "operator": "Equal", "valueInt": proposal_id},
                    {"path": ["chunk_number"], "operator": "Equal", "valueNumber": chunk_number}
                ]
            }
            
            # Execute the query
            result = client.query.get("RFP").with_where(where_filter).with_additional("id").do()
            print(f"Query result: {result}") 
            objects = result['data']['Get']['RFP'] if result and 'data' in result else []

            if objects:
                object_id = objects[0]['_additional']['id']
                print(f"Updating existing chunk with ID: {object_id} for chunk_number: {chunk_number}")
                data_object = {
                    "text": slice_,
                    "rfp_id": rfp_id,
                    "proposal_id": proposal_id,
                    "chunk_number": chunk_number,
                    "user_id": user_id,
                    "company_id": company_id
                }
                client.data_object.update(data_object, class_name="RFP", uuid=object_id)
                print(f"Updated chunk {chunk_number} for RFP ID: {rfp_id}, Proposal ID: {proposal_id}")

            else:
                print(f"No existing chunk found for chunk_number: {chunk_number}. Creating new chunk.")
                data_object = {
                    "text": slice_,
                    "rfp_id": rfp_id,
                    "proposal_id": proposal_id,
                    "chunk_number": chunk_number,
                    "user_id": user_id,
                    "company_id": company_id
                }
                client.data_object.create(data_object, "RFP")
                print(f"Inserted new chunk {chunk_number} for RFP ID: {rfp_id}, Proposal ID: {proposal_id}")

    except Exception as e:
        print(f"An error occurred while saving to Weaviate: {e}")





# Main function to handle PDF/Word, extract, slice, and save to Postgres and Weaviate
def process_and_store_document(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_word(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .pdf or .docx file.")
    
    text_slices = slice_text(text)