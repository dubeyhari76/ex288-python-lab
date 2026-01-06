FROM registry.access.redhat.com/ubi8/python-39

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY finance_app.py .

# Environment variables defaults (can be overridden)
ENV WELCOME_MSG="Welcome to Finance Portal"
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "finance_app:app"]
