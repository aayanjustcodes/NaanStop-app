import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
import json
import random

# Settings
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10
DATASET_PATH = "dataset/train"

# Load dataset
train_dataset = datasets.ImageFolder(
    DATASET_PATH,
    transform=transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
)

val_dataset = datasets.ImageFolder(
    DATASET_PATH,
    transform=transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
)

# Split indices manually
indices = list(range(len(train_dataset)))
random.shuffle(indices)
split = int(0.8 * len(indices))
train_indices = indices[:split]
val_indices = indices[split:]

train_loader = torch.utils.data.DataLoader(
    torch.utils.data.Subset(train_dataset, train_indices),
    batch_size=BATCH_SIZE, shuffle=True
)
val_loader = torch.utils.data.DataLoader(
    torch.utils.data.Subset(val_dataset, val_indices),
    batch_size=BATCH_SIZE, shuffle=False
)

# Save class labels
class_labels = {v: k for k, v in train_dataset.class_to_idx.items()}
with open("class_labels.json", "w") as f:
    json.dump(class_labels, f)
print("Class labels saved.")
print(f"Training samples: {len(train_indices)}, Validation samples: {len(val_indices)}")

# Load MobileNetV2 pretrained model
model = models.mobilenet_v2(weights="IMAGENET1K_V1")

# Freeze base layers
for param in model.parameters():
    param.requires_grad = False

# Replace classifier head
num_classes = len(train_dataset.classes)
model.classifier[1] = nn.Linear(model.last_channel, num_classes)

# Training setup
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Training on: {device}")
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

# Training loop
for epoch in range(EPOCHS):
    print(f"Epoch {epoch+1} starting, batches: {len(train_loader)}")
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    train_acc = 100. * correct / total

    # Validation
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            val_total += labels.size(0)
            val_correct += predicted.eq(labels).sum().item()

    val_acc = 100. * val_correct / val_total
    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(train_loader):.3f} - Train Acc: {train_acc:.1f}% - Val Acc: {val_acc:.1f}%")

# Save model
torch.save(model.state_dict(), "model.pth")
print("Model saved as model.pth")