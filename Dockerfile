FROM public.ecr.aws/lambda/python:latest

# Copy requirements.txt
COPY app/requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy function code
COPY app/main.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.handler" ]