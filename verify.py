from collections import Counter
from torchvision.datasets import ImageFolder

dataset = ImageFolder("dataset/wheat/train")
print(Counter([label for _, label in dataset]))
