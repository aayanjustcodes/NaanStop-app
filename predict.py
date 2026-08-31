import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json

IMG_SIZE = 224

def load_model():
    with open("class_labels.json", "r") as f:
        class_labels = json.load(f)
    
    num_classes = len(class_labels)
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    model.load_state_dict(torch.load("model.pth", map_location="cpu"))
    model.eval()
    
    return model, class_labels

def predict_dish(image_path):
    model, class_labels = load_model()
    
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(image)
        _, predicted = outputs.max(1)
        dish_name = class_labels[str(predicted.item())]
    
    return dish_name

if __name__ == "__main__":
    image_path = input("Enter the path to your food image: ")
    dish = predict_dish(image_path)
    print(f"Predicted dish: {dish}")