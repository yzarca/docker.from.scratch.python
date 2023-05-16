# docker.from.scratch.pytho

### simpleapi:ZIP.3.0.1

``` dockerfile
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
```

``` sh
cat requirements.txt
```

>```
>flask
>patchelf-wrapper
>pyinstaller
>requests
>scons
>staticx
>```

``` sh
docker build -f Dockerfile -t simpleapi:ZIP.3.0.1 .
docker run -it -p 8082:5000 --name simpleapi_02 simpleapi:ZIP.3.0.1
docker run --rm -d -p 8081:5000 --name simpleapi-zip-01 simpleapi:ZIP.3.0.1
#
docker image ls | grep simpleapi | sort
```

```
simpleapi                    ZIP.3.0.0   ad919f96f188   2 hours ago         10.4MB
simpleapi                    ZIP.3.0.1   32447c0d34e1   About an hour ago   9.45MB
#
yz.registry:5000/simpleapi   ZIP.2.1.0   25492a0138d0   2 days ago          15.9MB
yz.registry:5000/simpleapi   ZIP.3.0.1   32447c0d34e1   About an hour ago   9.45MB
```

``` sh
docker tag simpleapi:ZIP.3.0.1 yz.registry:5000/simpleapi:ZIP.3.0.1
docker push yz.registry:5000/simpleapi:ZIP.3.0.1
```
