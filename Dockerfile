FROM public.ecr.aws/lambda/python:latest

# Set working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Set the command
CMD ["main.lamda_handler"]