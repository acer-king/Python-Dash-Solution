FROM python:3

WORKDIR /usr/local/

# Install dependencies:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python plot.py
