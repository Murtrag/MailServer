FROM python:3
# RUN mkdir /code
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
# RUN python3 setup.py
# CMD ['python']

