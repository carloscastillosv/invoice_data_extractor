from dotenv import load_dotenv
from openai import OpenAI

import os
import time
import logging


load_dotenv(override=True)  # Load environment variables from .env file
api_key = os.getenv("OPENAI_API_KEY")
amz_assistant_id = os.getenv("AMZ_ASSISTANT_ID")

if not api_key or not amz_assistant_id:
    raise ValueError("OPENAI_API_KEY and AMZ_ASSISTANT_ID must be set in the environment variables.")

def call_openai_assistant(pdf_text: str) -> str:
    """
    Calls the OpenAI API with a specific assistant ID.
    
    Args:
        assistant_id (str): The ID of the assistant to use.
        prompt (str): The prompt to send to the assistant.
        pdf_text (str): The text extracted from the PDF.
        
    Returns:
        str: The response from the OpenAI API.
    """
    
    client = OpenAI()
    asistant_id = amz_assistant_id

    # print(asistant_id)

    # Create a thread and run it with the assistant
    thread_id = client.beta.threads.create()

    # Create a message in the thread with the PDF text
    thread_message = client.beta.threads.messages.create(
        thread_id=thread_id.id,
        role="user",
        content=pdf_text,
    )

    # Start a run in the thread with the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id.id,
        assistant_id=asistant_id
        
    )

    # Response variable to hold the response
    response = None

    while True:
        try:
            run_retrieve = client.beta.threads.runs.retrieve(thread_id=thread_id.id, run_id=run.id)
            if run_retrieve.completed_at:
                elapsed_time = run_retrieve.completed_at - run_retrieve.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id.id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                logging.info(f"Run completed in {formatted_elapsed_time}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break

        print("Waiting for run to complete...")
        time.sleep(3)

    return response
    