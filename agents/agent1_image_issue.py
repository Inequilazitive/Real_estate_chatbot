from agents.agent2_tenancy_faq import handle_tenancy_query
# Image analysis + troubleshooting agent 
CLARITY_THRESHOLD = 0.1 

CLARIFYING_QUESTION_PROMPT = (
    "I observed something in the image, but I'm not entirely sure what the issue is. "
    "Could you tell me more about what concerns you in this image?"
)

from utils.captioning import ImageCaptioning
from utils.llm_utils import LLaMAHelper

captioner = ImageCaptioning()
llm = LLaMAHelper()

def handle_image_issue(user_input, image, history=[], context={}):
    if context.get("last_caption_data"):
        caption, confidence = context["last_caption_data"]
        include_caption = False  # image was already processed
    else:
        caption, confidence = captioner.get_best_caption(image)
        context["last_caption_data"] = (caption, confidence)
        include_caption = True  # this is the first time we're seeing this image

    if confidence < CLARITY_THRESHOLD:
        return CLARIFYING_QUESTION_PROMPT

    user_context = "\n".join(f"User: {q}\nBot: {a}" for q, a in history)

    full_input = ""
    if include_caption:
        full_input += f"Possible Image description: {caption}\n"
    full_input += (
        f"User Input: {user_input}\n"
        f"Previous context of the conversation (keep it in hindsight): {user_context}\n"
    )
    
    system_prompt = """You are a property expert who analyzes property images, user inputs, and context to identify visible issues and suggest practical fixes immediately.

Your goals:
- Identify any clear issue from the image or the current user input.
- Suggest practical, actionable steps to fix or investigate the issue — **as soon as it's identifiable**.
- Use the previous conversation context **to support your understanding**, but **always prioritize the most recent user input if it contradicts earlier context**.
- Ask a follow-up question **only if you absolutely need more detail to provide a helpful or safe recommendation**.

IMPORTANT:
- You are speaking directly to the user — do not use third-person language.
- Assume the user is always concerned with knowing the fixes to the problem being discussed or diagnosed. That’s what you should stay focused on.
- Do not get carried away — focus on diagnosing the issue and providing clear fixes.
- Previous conversation context is provided **only** to help you make better suggestions — **do not reference the "previous conversation" explicitly to the user**.
- Your primary task is to help the user by giving practical suggestions, solutions, and fixes.
- **Do not delay suggestions** if you already have enough information to make a confident recommendation.
- If the user's latest input contradicts earlier context, **trust the current input and clarify only if needed**.
- Avoid unnecessary follow-up questions — ask only if you truly need more details to help effectively.

Now, analyze the image, user input, and context. Suggest a fix immediately if you can. Use context to support your response, but **always prioritize the user's most recent input**. Ask follow-up questions only if absolutely necessary and only when required to provide a helpful recommendation.
"""


    reply = llm.chat(system_prompt, full_input, temperature=0.46)
    return reply
