FROM python:3.12-slim

WORKDIR /app

# Install the package (pure-Python, no system deps needed)
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8000

# Run the local web UI; bind to 0.0.0.0 so the port mapping works
CMD ["saudi-gov-web", "--host", "0.0.0.0", "--port", "8000"]
