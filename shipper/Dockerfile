FROM python:3.10-slim
WORKDIR /shipper
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY shipper.py .
CMD ["python", "shipper.py"]

