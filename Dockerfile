# BUILD
FROM python:3.10-slim AS build
WORKDIR "/app"
RUN apt-get update ; \
    apt-get install binutils build-essential gcc libc-bin patchelf -y ; \
    apt-get clean ;
ADD requirements.txt requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip ; \
    python -m pip install --no-cache-dir --upgrade -r requirements.txt ;
ADD simpleapi.py simpleapi.py
RUN pyinstaller --onefile --name simpleapi simpleapi.py ; \
    cd dist ; \
    staticx simpleapi simpleapi ;

# RELEASE
FROM scratch
WORKDIR "/app"
COPY tmp /tmp
COPY --from=build /app/dist/simpleapi /app/simpleapi
ENTRYPOINT [ "/app/simpleapi" ]
