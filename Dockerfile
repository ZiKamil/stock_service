FROM python:3.9

COPY /stock .

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

RUN chmod +x "./entrypoint.sh"
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]