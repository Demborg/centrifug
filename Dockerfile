FROM python:3.9
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD server.py server.py
CMD [ "python3", "-m" , "flask", "--app", "server.py", "run", "--host=0.0.0.0"] 
