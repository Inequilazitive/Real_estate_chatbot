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

## Overview

This project is a multi-agent chatbot designed for the real estate domain. It intelligently handles both text-based tenancy FAQs and image-based property issue troubleshooting. Users can interact with the chatbot by typing questions or uploading images, and the system will automatically determine the best agent to respond — whether it's a legal assistant for tenancy issues or an image-based troubleshooting expert.

# 🏡 Real Estate Chatbot – How to Use

This guide will walk you through the steps to launch and interact with the Real Estate Chatbot using Google Colab. The chatbot is hosted in the GitHub repository:  
👉 **[https://github.com/Inequilazitive/Real_estate_chatbot](https://github.com/Inequilazitive/Real_estate_chatbot)**

---

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TRLb8VpUZeBlFoCk9HwXn4gt3jY5TIAn?usp=sharing)

## 🚀 Step-by-Step Instructions

### 1. **Open the Notebook in Google Colab**
- Open the Jupyter notebook file attached with this guide named `Use-real-estate-chatbot.ipynb` or available in the GitHub repository.
- Use **Google Colab** to run the notebook.

### 2. **Connect to a T4 GPU**
- In Colab, go to **Runtime > Change runtime type**.
- Select **GPU** as the hardware accelerator and ensure it's a **T4 GPU** for optimal performance.

### 3. **Run Notebook Cells One by One**

#### ✅ **Step 1: Clone the GitHub Repository**
```python
!git clone "https://github.com/Inequilazitive/Real_estate_chatbot"
```

#### ✅ **Step 2: Change Directory**
```python
%cd '/content/Real_estate_chatbot'
```

#### ✅ **Step 3: Set Hugging Face Access Token**
```python
import os
os.environ["HF_TOKEN"] = "<Your HF access token with access to llama 3.2-3B-Instruct model>"

```
#### ✅ **Step 4: Run the App**
```python
!python3 app.py
```

## 💬 Access the Chatbot

After the app launches, look for the output that includes two URLs:
- A **local URL** (usually starting with `http://127.0.0.1`)
- A **public URL** (starting with something like `https://xxxx.gradio.live`)

👉 Click on the **public URL** to open and interact with the chatbot.

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

### 3. **Hugging Face- BLIP + GIT + CLIP Ensemble**
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

### 6. **Hugging Face - LLaMA (Language Model for Multiple Agents)**
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

## Storage and GPU Limitations: Compromises and Future Work

While designing and developing this system, we encountered several constraints due to limited computational resources—especially GPU memory, CPU power, and local/Colab-based VRAM and storage limits. These resource limitations impacted multiple aspects of the solution architecture, leading to compromises in model choice and design. Below are key instances where compromises were made and the proposed future work to address them:

---

### 1. Model Selection for Text Generation

Initially, we aimed to use powerful large language models (LLMs) for text generation tasks. However, due to storage and compute limitations, we opted for a smaller variant of the LLaMA model. LLaMA models are generally known for their strong performance in text generation tasks and are open source—making them ideal for POC-level work.

- **Compromise**: Used a lightweight LLaMA variant for local compatibility.
- **Future Work**: Once resources are scaled, we intend to incorporate larger LLaMA models (e.g., `llama-3.1-8b-instruct`) or explore commercial models like GPT-4o or Claude (Anthropic) for enhanced performance and naturalness in generated outputs.

---

### 2. Zero-shot Text Classification for Agent Routing

A critical planned feature was dynamic agent switching based on conversation context. For example, if a user, while discussing an image, begins asking tenancy-related questions, a classification pipeline would detect the intent and automatically switch to a relevant agent, passing along the full context. Initially, we used `facebook/bart-large-mnli` for this zero-shot classification task.

- **Compromise**: Due to low GPU/CPU/VRAM availability on local setups and Google Colab, we had to remove this functionality.
- **Future Work**: With access to more powerful hardware or inference APIs, we can reintegrate this feature, significantly improving conversation flow and user experience.

---

### 3. Multi-model Output Scoring Pipeline

To boost output quality, we planned to simultaneously generate responses using both LLaMA and Mistral models, and then run a scoring mechanism to select the most relevant response.

- **Compromise**: Resource constraints made it infeasible to load and run multiple LLMs in parallel.
- **Future Work**: Revisit the multi-model setup once better hardware (or hosted services) are available. This will allow ensemble-style approaches for higher quality text generation and response reliability.


This detailed overview describes the tools and logic behind the switching mechanism that allows the chatbot to provide contextual and multimodal support effectively.
