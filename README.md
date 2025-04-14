---
title: Real Estate Agent Chatbot
emoji: 🌖
colorFrom: gray
colorTo: pink
sdk: gradio
sdk_version: 5.25.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Smart chatbot for tenancy and property image issues.
---

# Multi-Agent Real Estate Chatbot – Detailed Explanation

## Tools & Technologies Used

### 1. **Gradio**
   - **Purpose**: Gradio is used to create the user interface for the chatbot. It allows quick and easy deployment of interactive web-based applications. The Gradio interface is designed to handle both text input and image uploads from the user.
   - **Features Used**: 
     - `gr.Textbox` for accepting text-based user queries.
     - `gr.Image` for handling image uploads.
     - `gr.Button` for triggering the input submission, starting a new chat, and clearing chat history.
     - `gr.State` for maintaining the chatbot’s session state, history, and user context across multiple interactions.

### 2. **Python**
   - **Purpose**: The core programming language for implementing the chatbot’s backend logic. Python’s flexibility and rich ecosystem of libraries make it suitable for integrating different models and tools into the chatbot system.

### 3. **BLIP + GIT + CLIP Ensemble**
   - **BLIP (Bootstrapping Language-Image Pre-training)**: 
     - **Purpose**: BLIP is used for generating captions from images. It combines vision and language models to interpret the content of the image and generate a descriptive caption.
     - **How It Works**: The BLIP model processes the image and outputs a textual description based on visual features. This serves as the first step in the image issue detection process.
   
   - **GIT (Grounded Image-to-Text)**: 
     - **Purpose**: GIT is used alongside BLIP to generate a different set of captions for the image. It focuses on aligning the image with grounded language models, producing captions grounded in both visual data and textual input.
     - **How It Works**: GIT’s primary goal is to generate diverse and grounded descriptions by considering both the image's visual content and the textual context from the conversation.
   
   - **CLIP (Contrastive Language-Image Pre-training)**:
     - **Purpose**: CLIP is used to rank and score the generated captions based on their relevance to the image. It evaluates how well the captions correspond to the visual content by calculating the similarity between image features and textual descriptions.
     - **How It Works**: CLIP uses its vision and language models to compare different caption candidates and select the one that is the most accurate, ensuring that the final caption best reflects the image's content.

### 4. **MD5 Hashing**
   - **Purpose**: MD5 hashing is used to detect changes in the uploaded image to prevent redundant processing. If the user uploads the same image more than once, it allows the system to avoid re-captioning it, saving computational resources and providing a quicker response.
   - **How It Works**: The MD5 hash of the image is computed by converting its pixel data into a unique string. If the hash is the same as the previously uploaded image’s hash, the system knows that the image has not changed and will skip reprocessing.

### 5. **Rule-Based Routing**
   - **Purpose**: Rule-based routing is used to determine which agent should handle the user query. The system decides whether the query should be handled by Agent 1 (image troubleshooting) or Agent 2 (tenancy FAQs).
   - **How It Works**: 
     - If the user uploads an image, the system automatically routes the query to **Agent 1**.
     - If the user query contains specific tenancy-related keywords (e.g., “rent”, “contract”, “lease”), the system routes the query to **Agent 2**.
     - In the case where the system cannot determine the appropriate agent, a fallback is provided, and the system defaults to Agent 2.

### 6. **LLaMA (Language Model for Multiple Agents)**
   - **Purpose**: LLaMA is a large-scale language model (specifically, LLaMA 3.2-3B-Instruct) used to generate responses for tenancy-related queries. It is capable of processing complex language inputs and delivering contextually appropriate responses.
   - **How It Works**: LLaMA is fine-tuned to understand tenancy law and property-related queries, allowing it to generate informative and accurate responses when the chatbot is in the tenancy FAQ mode.

### 7. **SpaCy & GeoText**
   - **Purpose**: These libraries are used for location extraction. The system uses **SpaCy** for Named Entity Recognition (NER) to detect locations in user input (e.g., city or country), and **GeoText** is used as a backup to detect locations in text, especially useful for informal or unstructured inputs.
   - **How It Works**: The system scans the user’s input for location-related keywords and uses either SpaCy or GeoText to extract a city or country name. This information is then used to personalize the response or narrow down the scope of tenancy-related advice.

---

## Logic Behind Agent Switching

### 1. **Image-Based Context** (Agent 1: Image Troubleshooter)
   - **Trigger**: If the user uploads an image, the system detects the presence of an image and routes the query to **Agent 1**. This agent is specialized in handling image-based issues, such as property damage or maintenance problems.
   - **Process**: 
     - The uploaded image is captioned using the **BLIP** and **GIT** models.
     - The caption is then scored using **CLIP** to determine its relevance.
     - If the caption provides sufficient information (with high confidence), **Agent 1** can immediately suggest practical fixes for the issue.
     - If the confidence is low, **Agent 1** asks clarifying questions to the user for more information.
   - **Use Case**: A user might upload a photo of a broken window or a leaking pipe, and the system will analyze the image and provide troubleshooting or maintenance advice.

### 2. **Text-Based Context** (Agent 2: Tenancy FAQ Assistant)
   - **Trigger**: If no image is uploaded or if the user asks a tenancy-related question, the system switches to **Agent 2**. This agent is responsible for providing legal information about property renting and tenancy laws.
   - **Process**: 
     - The user’s input is checked for keywords related to tenancy, such as "lease", "rent", "tenant", or "landlord".
     - The system also attempts to extract location information from the query (if not already provided by the user) to offer location-specific advice.
     - If the query is tenancy-related, **Agent 2** uses the **LLaMA** language model to generate a response, often with a focus on legal aspects of renting or property management.
   - **Use Case**: A user might ask about the process for returning a security deposit or inquire about tenant rights in a specific city or country.

### 3. **Agent Switching Based on Context**
   - **Seamless Switching**: The system can seamlessly switch between **Agent 1** and **Agent 2** based on the content of the user’s query.
   - **Image Context to Text Context**: If the user uploads an image but later asks a tenancy-related question, the system will automatically switch to **Agent 2**.
   - **Text Context to Image Context**: If a user initially asks a text-based question but then uploads an image, the system will switch to **Agent 1** for image issue troubleshooting.

### 4. **Context Preservation and History Management**
   - The chatbot maintains a history of both user inputs and responses, which helps to preserve the context of the conversation.
   - **Image Context**: If the user uploads an image and switches to a tenancy query, the image context is preserved for future reference. If a new image is uploaded, the history is reset, and the system starts fresh.

### 5. **Fallback to Tenancy FAQ Agent**
   - If the system is unable to determine the appropriate agent (e.g., unclear input), it defaults to **Agent 2**, which handles tenancy-related queries. This ensures that the chatbot can always provide a helpful response, even in ambiguous situations.

---

This detailed overview describes the tools and logic behind the switching mechanism that allows the chatbot to provide contextual and multimodal support effectively.
