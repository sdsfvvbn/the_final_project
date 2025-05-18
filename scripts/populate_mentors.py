import os
import django
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Ganti 'yourproject' sesuai nama folder project kamu (yang ada settings.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from category.models import Mentor
from django.core.files.base import ContentFile
import requests

names = ['Alan', 'Lisa', 'Tom', 'Anna']
titles = ['Digital Painter', 'Music Teacher', 'Yoga Trainer', 'Math Tutor']
locations = ['Taipei', 'Tainan', 'Kaohsiung']
modes = ['Online', 'Meet in Person']

def generate_avatar():
    response = requests.get('https://i.pravatar.cc/150', timeout=10)
    return ContentFile(response.content, 'avatar.jpg')

def run():
    for i in range(10):
        mentor = Mentor(
            name=random.choice(names),
            title=random.choice(titles),
            location=random.choice(locations),
            mode=random.choice(modes),
        )
        mentor.avatar.save(f'avatar_{i}.jpg', generate_avatar(), save=True)

    print("Dummy mentors created!")

if __name__ == '__main__':
    run()
