FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY src/ src/
EXPOSE 8090 8091
HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD curl -f http://localhost:8090/health || exit 1
CMD ["python", "-m", "src.main"]
