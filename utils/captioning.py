from transformers import BlipProcessor, BlipForConditionalGeneration, AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch
from ultralytics import YOLO  # You need to install: pip install ultralytics
from transformers import CLIPProcessor, CLIPModel

class ImageCaptioning:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load BLIP
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)

        # Load GIT
        self.git_processor = AutoProcessor.from_pretrained("microsoft/git-base")
        self.git_model = AutoModelForCausalLM.from_pretrained("microsoft/git-base").to(self.device)
        
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)

        # # Load YOLO
        # self.yolo_model = YOLO("yolov8n.pt")  # You can use yolov8s.pt or others

    def generate_caption_blip(self, image):
        inputs = self.blip_processor(images=image, return_tensors="pt").to(self.device)
        print(f"Inputs keys: {inputs.keys()}")
        with torch.no_grad():
            output = self.blip_model.generate(**inputs)
        caption = self.blip_processor.decode(output[0], skip_special_tokens=True)
        return caption, self.compute_logprob(self.blip_model, inputs, output, self.blip_processor)
    
    def generate_caption_git(self, image):
        inputs = self.git_processor(images=image, return_tensors="pt").to(self.device)
        print(f"Inputs keys: {inputs.keys()}")
        with torch.no_grad():
            generated_ids = self.git_model.generate(**inputs)
        caption = self.git_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return caption, self.compute_logprob(self.git_model, inputs, generated_ids, self.git_processor)

    # def generate_caption_yolo(self, image):
    #     # Run YOLO detection
    #     results = self.yolo_model(image)
    #     detections = results[0].boxes.data  # [x1, y1, x2, y2, conf, class]
    #     names = results[0].names

    #     if len(detections) == 0:
    #         return "No objects detected", 0.0

    #     # Get top class labels with confidence
    #     label_conf_pairs = [(names[int(cls)], float(conf)) for *_, conf, cls in detections]
    #     label_conf_pairs.sort(key=lambda x: x[1], reverse=True)

    #     top_labels = list({label for label, _ in label_conf_pairs[:5]})  # top 5 unique labels
    #     avg_conf = sum([conf for _, conf in label_conf_pairs[:5]]) / len(top_labels)

    #     caption = "Image contains: " + ", ".join(top_labels)
    #     return caption, avg_conf
    
    def generate_caption_clip(self, image):
        # Step 1: Generate caption candidates
        caption_blip = self.generate_caption_blip(image)
        caption_git = self.generate_caption_git(image)
        candidates = [caption_blip, caption_git]

        # Extract text-only for CLIP scoring
        captions_only = [c[0] for c in candidates]

        # Step 2: Score them with CLIP
        inputs = self.clip_processor(text=captions_only, images=image, return_tensors="pt", padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.clip_model(**inputs)
            scores = outputs.logits_per_image[0]  # shape: (num_captions,)
            scores = scores.softmax(dim=0)  # optional: normalize scores

        best_idx = scores.argmax().item()
        best_caption = candidates[best_idx]
        best_score = scores[best_idx].item()

        return best_caption[0], best_score  # returning the caption text and score


    def compute_logprob(self, model, inputs, generated_ids, processor):
        # Decode the generated tokens to text
        caption_text = processor.decode(generated_ids[0], skip_special_tokens=True)

        # Tokenize the caption (text) to get labels and input_ids
        text_inputs = processor(text=caption_text, return_tensors="pt").to(self.device)
        labels = text_inputs["input_ids"]

        # Combine image inputs with the new input_ids (needed for loss computation)
        model_inputs = {**inputs, "input_ids": text_inputs["input_ids"]}

        # Compute the loss
        with torch.no_grad():
            outputs = model(**model_inputs, labels=labels)

        return -outputs.loss.item()  # Higher is better



    def get_best_caption(self, image):
    # This runs BLIP and GIT, then scores both with CLIP to pick the best caption
        caption, score = self.generate_caption_clip(image)
        print(f"Selected Caption: {caption} | Confidence: {score}")
        return caption, score

