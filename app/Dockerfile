# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variable to avoid debconf warnings
ARG DEBIAN_FRONTEND="noninteractive"
ARG DEBCONF_NOWARNINGS="yes"

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install necessary packages
RUN apt-get update
RUN apt-get -qq -y --no-install-recommends install apt-utils
RUN apt-get -qq -y --no-install-recommends install gcc
RUN apt-get -qq -y --no-install-recommends install linux-libc-dev
RUN apt-get -qq -y --no-install-recommends install libc6-dev
RUN apt-get -qq -y --no-install-recommends install build-essential
RUN apt-get -qq -y --no-install-recommends install portaudio19-dev
RUN apt-get -qq -y --no-install-recommends install python3-pyaudio
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "app.py"]
