FROM python:3.10-slim
WORKDIR /render_template_aws
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
