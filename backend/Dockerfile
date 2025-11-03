# STAGE 1 : Builder - Install Dependencies
FROM python:3.11-slim as builder

# Set the working directory for the application code
WORKDIR /app

# Copy the requirements file first to take care of DOCKER Caching.
COPY requirements.txt .

# Install Dependencies
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2 : Production - Create the final image
FROM python:3.11-slim

WORKDIR /app

# Copy the packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the executables (uvicorn) from builder
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



