import google.auth
import os

file_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if os.path.exists(file_path):
    print("File found!")
else:
    print("File not found!")

try:
    credentials, project_id = google.auth.default()
    print(f"Credentials loaded successfully. Project ID: {project_id}") 
except Exception as e:
    print(f"Error loading credentials: {e}")