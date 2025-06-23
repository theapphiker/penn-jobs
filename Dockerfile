# Use a Python base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app


# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    tar \
    bzip2 \
    xvfb \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libnss3 \
    libasound2 \
    libxrandr2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrender1 \
    libxtst6 \
    && rm -rf /var/lib/apt/lists/*


# Set environment variable for Geckodriver version
ENV GECKODRIVER_VERSION=0.36.0 

RUN wget --no-verbose -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz" && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    rm /tmp/geckodriver.tar.gz && \
    chmod +x /usr/local/bin/geckodriver

# Copy your Python scripts
COPY src/psu_jobs.py .
COPY src/penn_jobs.py .

# Command to run your script when the container starts
CMD python -u psu_jobs.py && python -u penn_jobs.py
