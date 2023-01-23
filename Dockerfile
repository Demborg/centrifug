FROM python:3.9-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY server.py server.py
CMD [ "python3", "-m" , "flask", "--app", "server.py", "run", "--host=0.0.0.0"] 
