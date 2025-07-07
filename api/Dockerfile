FROM python:3.11-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /src
RUN  pip install --no-cache-dir poetry
COPY pyproject.toml* poetry.lock* ./
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi
COPY  . . 
ENTRYPOINT [ "poetry", "run", "uvicorn","main:app","--host","0.0.0.0","--reload","--port","8000"]
# RUN tail /dev/null