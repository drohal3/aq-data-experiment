FROM python:3.11
WORKDIR /app
COPY . .
# CMake is needed to build and install awscrt from source
RUN apt-get update && apt-get -y install cmake
RUN pip install -r ./requirements.txt
CMD ["python", "./main.py"]