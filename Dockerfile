# ---- Base python ----
FROM python:3.12.2-slim
# Create app directory
WORKDIR /app
RUN apt update
RUN apt install -y coinor-cbc \
 && rm -rf /var/lib/apt/lists/*
# ---- Dependencies ----
# FROM base AS dependencies  
COPY requirements.txt ./
# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
# FROM dependencies AS build  
# WORKDIR /app
COPY ./src /app/src
# Build / Compile if required

# --- Release with Alpine ----
# FROM python:3.12.2-alpine3.19 AS release  
# Create app directory
# WORKDIR /app

# COPY --from=dependencies /app/requirements.txt ./
# COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
# RUN pip install -r requirements.txt
# COPY --from=build /app/ ./

#Copy the gunicorn config file
COPY gunicorn_config.py ./
CMD ["gunicorn", "--config", "./gunicorn_config.py", "src.main:app"]
