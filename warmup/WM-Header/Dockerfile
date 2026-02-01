# ──────────────────────────────────────────
# LKSWNSB CTF — Header Juggling Challenge
# ──────────────────────────────────────────
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY templates/ templates/

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
