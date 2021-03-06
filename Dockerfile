# Use an official python image
FROM python:3.7-stretch

# Set the working directory in the container to /app
WORKDIR /app

COPY requiments.txt /app/


#Install packets on build parts
RUN pip install -r requiments.txt
RUN apt update 
RUN apt-get -y install libreoffice  
RUN mkdir qrs
RUN mkdir docs
RUN mkdir pdfs

# Copy the current directory contents into the container at /app
ADD . /app

# Make the container's port 80 available to the outside world
EXPOSE 80

# Run serv.py using python when the container launches
CMD ["stdbuf", "-oL","python","serv.py"]
