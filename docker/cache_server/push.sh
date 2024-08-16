# docker run --rm test
bazel run //docker/cache_server:server_image_tarball
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin us-central1-docker.pkg.dev
docker tag local us-central1-docker.pkg.dev/stocker-416721/server/cache-server:golden
docker push us-central1-docker.pkg.dev/stocker-416721/server/cache-server:golden