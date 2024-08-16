# docker run --rm local
docker build -t local -f docker/data_import_jobs/prod/Dockerfile .
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin us-central1-docker.pkg.dev
docker tag local us-central1-docker.pkg.dev/stocker-416721/data-jobs/daily-importer:golden
docker push us-central1-docker.pkg.dev/stocker-416721/data-jobs/daily-importer:golden