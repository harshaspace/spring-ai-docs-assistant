FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

# Copy the whole project
COPY . .

# Install dependencies
RUN uv sync --frozen

# Use the virtual environment created by uv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "src/startup.py"]