set -e
python3 -m pip -q install pre-commit
pre-commit install

IMAGE_NAME=`echo "print '$(basename $(pwd))'.lower()" | python`
docker build -f docker/Dockerfile -t $IMAGE_NAME .
docker run -it --rm -w /app -v $(pwd):/app -p 5000:5000 --entrypoint /bin/bash $IMAGE_NAME
