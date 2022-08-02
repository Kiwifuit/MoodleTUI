# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.4-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc libffi-dev musl-dev && pip install cython cffi && apk del .build-deps gcc libffi-dev musl-dev
RUN pip install -r requirements.txt

ADD res .
WORKDIR /src

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /src
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "src/main.py"]
