FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["sh","-c", "python3 test_task_VK/manage.py migrate && python3 test_task_VK/manage.py loadstatus && python3 test_task_VK/manage.py runserver 0:8000"] 