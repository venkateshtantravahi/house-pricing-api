# 1. Base Image: Start with a lightweight version of Python
FROM python:3.9-slim

# 2. Work Directory: Create a folder inside the container
WORKDIR /app

# 3. Dependencies: Install libraries first
# We copy requirements.txt separately to leverage Docker's "Layer Caching".
# This makes re-building the container much faster if only your code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Application Code: Copy the rest of your files
COPY . .

# 5. Launch: Start the Flask server
# We bind to 0.0.0.0 to ensure the container listens to external requests.
CMD ["python", "app.py"]