FROM python:3.10-slim

# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY ../pyproject.toml .
COPY ../poetry.lock .
# Install dependencies
RUN pip install poetry==2.1.3
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --without dev

COPY ../ .

# Expose the port the app runs on
EXPOSE 8000
# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8000"]
