# agent_router.py
import re

# Router to manage multi-agent classification
# agent_router.py
import re

def route_agent(text, has_image):
    """
    Determines which agent should handle the query based on image presence and content type.
    """
    if has_image:
        return "agent1"  # Image-based input => Image issue agent

    # Check for tenancy-related keywords
    tenancy_keywords = [
        "rent", "lease", "tenant", "landlord", "agreement", "deposit",
        "eviction", "notice", "contract", "housing law", "tenancy", "sublet"
    ]

    # Lowercase and look for keywords
    if any(word in text.lower() for word in tenancy_keywords):
        return "agent2"

    # Fallback — you could route this to a clarification step instead
    return "agent2"

def clarify_prompt():
    return (
        "Just to clarify, are you asking about a visible issue with a property (you can also upload an image),\n"
        "or is this a general question about renting, laws, or agreements?"
    )
