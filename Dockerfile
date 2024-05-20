FROM python:3.8.10-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7755 available to the world outside this container
EXPOSE 7755

# Define environment variable
ENV FLASK_APP core/server.py
ENV FLASK_ENV production

# Run run.sh when the container launches
CMD ["./run.sh"]