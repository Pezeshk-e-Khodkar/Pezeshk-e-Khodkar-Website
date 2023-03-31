FROM ubuntu:jammy

# Create project directory
WORKDIR /usr/src/PezeshkeKhodkarAPI

# Copy project
COPY . .


# Install tools:
RUN apt update --fix-missing\
    &&  apt --assume-yes install python3 \
    &&  apt --assume-yes install python3-pip \
    &&  pip install -r requirements.txt --timeout 10000

# Specify that the application in the container listens on port 8000
EXPOSE 8000

# Start!
CMD python3 ./manage.py runserver
