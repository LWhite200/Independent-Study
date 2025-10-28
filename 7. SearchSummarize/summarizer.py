# summarizer.py
import google.generativeai as genai

def summarize_text(text, model_name="models/gemini-flash-latest"): # Changed 'model' to 'model_name' to avoid conflict
    """
    Summarize long text using the current Google Gemini API.
    Works with google-generativeai v0.8.5.
    """
    if not text.strip():
        return "(No content found to summarize.)"

    model = genai.GenerativeModel(model_name) # Initialize the model
    response = model.start_chat(history=[]).send_message( # Start a chat and send the message
        f"Summarize this clearly into key points:\n{text}"
    )

    return response.text # Access the text directly from the response