# 🏡 Real Estate Chatbot – How to Use

This guide will walk you through the steps to launch and interact with the Real Estate Chatbot using Google Colab. The chatbot is hosted in the GitHub repository:  
👉 **[https://github.com/Inequilazitive/Real_estate_chatbot](https://github.com/Inequilazitive/Real_estate_chatbot)**

---

## 🚀 Step-by-Step Instructions

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1TRLb8VpUZeBlFoCk9HwXn4gt3jY5TIAn?usp=sharing)

### 1. **Open the Notebook in Google Colab**
- Open the colab link attached OR Open the Jupyter notebook file attached with this guide named 'Use-real-estate-chatbot.ipynb' on google colab OR access the notebook in the GitHub repository and open via google colab.

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
> Ensure you have access to the LLaMA model repository on Hugging Face.

```python
import os
os.environ["HF_TOKEN"] = "<Your HF access token with access to llama 3.2-3B-Instruct model>"
```

#### ✅ **Step 4: Run the App**
```python
!python3 app.py
```

---

## 💬 Access the Chatbot

After the app launches, look for the output that includes two URLs:
- A **local URL** (usually starting with `http://127.0.0.1`)
- A **public URL** (starting with something like `https://xxxx.gradio.live`)

👉 Click on the **public URL** to open and interact with the chatbot.
