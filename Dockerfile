# Use an official python image
FROM python:3.7-stretch

# Set the working directory in the container to /app
WORKDIR /app

#Install packets on build parts
RUN pip install pandas
RUN pip install docxtpl
RUN pip install qrcode
RUN pip install xlrd 
RUN pip install openpyxl
RUN apt update 
RUN apt-get -y install libreoffice  
RUN mkdir qrs
RUN mkdir docs
RUN mkdir pdfs
RUN pip install Image
RUN pip install requests


# Copy the current directory contents into the container at /app
ADD . /app

VOLUME /var/dockerlog /app/out

# Make the container's port 80 available to the outside world
EXPOSE 80

# Run serv.py using python when the container launches
CMD ["python","serv.py"]
