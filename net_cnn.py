import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn.functional as F
from PIL import Image

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        
        # Define the CNN architecture
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=3, stride=2, padding=0)
        
        # Fully connected network for classification
        self.fc1 = nn.Linear(16 * 127 * 127 + 32 * 63 * 63 + 64 * 31 * 31, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 1)
        
        # Transformation to be applied to the images
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        # Loss function and optimizer
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.parameters(), lr=0.1)
    
    def forward(self, x):
        print("Input shape:", x.shape)
        x1 = self.pool(F.relu(self.conv1(x)))
        print("After conv1 and pool:", x1.shape)
        x2 = self.pool(F.relu(self.conv2(x1)))
        print("After conv2 and pool:", x2.shape)
        x3 = self.pool(F.relu(self.conv3(x2)))
        print("After conv3 and pool:", x3.shape)
        
        # Flatten and concatenate
        x1 = x1.view(x1.size(0), -1)
        x2 = x2.view(x2.size(0), -1)
        x3 = x3.view(x3.size(0), -1)
        x = torch.cat((x1, x2, x3), dim=1)
        print("After concatenation:", x.shape)
        
        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x)) * 100  # Scale to [0, 100]
        return x
    
    def eval_image(self, image_path):
        image = Image.open(image_path)
        image = self.transform(image)
        image = image.unsqueeze(0)
        with torch.no_grad():
            output = self.forward(image)
        print("AI rating:", output.item())
        return output.item()
    
    def train_step(self, image, rating):
        self.optimizer.zero_grad()
        output = self.forward(image)
        loss = self.criterion(output, rating.float().unsqueeze(1))
        loss.backward()
        self.optimizer.step()
        return loss.item()
    
    def train_image(self, image_path, rating):
        image = Image.open(image_path)
        image = self.transform(image)
        image = image.unsqueeze(0)
        rating = torch.tensor([rating])
        return self.train_step(image, rating)
