import subprocess
import sys
import os

# Install requirements if needed
requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

import gradio as gr
from utils.routing import route_agent
from agents.agent1_image_issue import handle_image_issue
from agents.agent2_tenancy_faq import handle_tenancy_query
from PIL import Image
import torch
import hashlib


# Helper to generate MD5 hash from image
def get_image_hash(image):
    return hashlib.md5(image.tobytes()).hexdigest()

# Main query handler
def handle_query(user_input, image=None, location='', history=[], context={}):
    try:
        response_ui_msg = ""

        # Initialize context if missing
        context.setdefault("images", [])
        context.setdefault("image_hashes", [])
        context.setdefault("last_agent", None)
        context.setdefault("last_caption_data", None)

        # If there's a new image
        if image is not None:
            new_hash = get_image_hash(image)
            if len(context["image_hashes"]) == 0 or new_hash != context["image_hashes"][-1]:
                context["images"].append(image)
                context["image_hashes"].append(new_hash)
                context["location"] = ""
                context["last_caption_data"] = None  # Reset cached caption
                response_ui_msg = "(New image attached. Starting image-related discussion.)"

        # If image is removed mid-chat
        if image is None and context["images"]:
            response_ui_msg = "(Image removed. Continuing as text-only query.)"

        # Use location if no image context
        if not context["images"] and location:
            context["location"] = location

        # Determine which agent should handle the query
        is_image_context = bool(context["images"])
        agent = route_agent(user_input, is_image_context)

        # Agent switch handling
        if context["last_agent"] == 'agent1' and agent == 'agent2':
            response_ui_msg += "\n(Switching to tenancy discussion based on your query...)"

        elif context["last_agent"] == 'agent2' and agent == 'agent1':
            response_ui_msg += "\n(Detected switch to image-based issue. Starting a new conversation...)"
            history.clear()
            context.clear()
            context["images"] = [image] if image else []
            context["image_hashes"] = [get_image_hash(image)] if image else []
            context["last_caption_data"] = None
            context["last_agent"] = None
            context["location"] = location or ""

        # Update current agent
        context["last_agent"] = agent

        # Run the correct agent
        if agent == 'agent1':
            if context["images"]:
                result = handle_image_issue(user_input, context["images"][-1], history, context)
            else:
                result = "No image found to analyze."
        else:
            result = handle_tenancy_query(user_input, {"location": context.get("location")}, history)

        # Add message to response
        if response_ui_msg:
            result = f"{response_ui_msg}\n\n{result}"

        history.append((user_input, result))
        return result, history, context, "🟢 Chat Ongoing"

    except RuntimeError as e:
        if "CUDA out of memory" in str(e):
            error_msg = "⚠️ CUDA Out of Memory! Please try again later or reduce the image size."
            return error_msg, history, context, "🔴 Error"
        else:
            raise e

# Reset function
def reset_chat():
    return "", "", None, [], {"location": "", "images": [], "image_hashes": []}, "🟡 New Chat Started", ""

# Clear just the conversation history
def clear_chat_history():
    return [], "", "🧹 Chat history cleared"

# Build the Gradio interface
with gr.Blocks() as demo:
    conversation_history = gr.State([])
    user_context = gr.State({"location": "", "images": [], "image_hashes": []})
    session_state = gr.State("🟡 New Chat Started")

    gr.Markdown("# 🏠 Multi-Agent Real Estate Chatbot")
    gr.Markdown("Ask about property issues (with images) or tenancy questions!")

    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="Enter your question:")
            location_input = gr.Textbox(label="Enter your city or country (optional):")
            image_input = gr.Image(type="pil", label="Upload an image (optional):")

            submit_btn = gr.Button("Submit")
            new_chat_btn = gr.Button("🔁 Start New Chat")
            clear_history_btn = gr.Button("🧹 Clear Chat History")

        with gr.Column():
            chatbot_output = gr.Textbox(label="Chatbot Response:", interactive=False, lines=8)
            session_indicator = gr.Textbox(label="Session Status", interactive=False)

    # Hook button logic
    submit_btn.click(
        handle_query,
        inputs=[user_input, image_input, location_input, conversation_history, user_context],
        outputs=[chatbot_output, conversation_history, user_context, session_indicator]
    )

    new_chat_btn.click(
        reset_chat,
        inputs=[],
        outputs=[user_input, location_input, image_input, conversation_history, user_context, session_indicator, chatbot_output]
    )

    clear_history_btn.click(
        clear_chat_history,
        inputs=[],
        outputs=[conversation_history, chatbot_output, session_indicator]
    )

# Launch app
demo.launch(share=True)
