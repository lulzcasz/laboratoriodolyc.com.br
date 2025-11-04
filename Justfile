export UV_ENV_FILE := ".env"

compose := "docker compose"
manage := "uv run manage.py"
minio := "docker compose exec -it storage mc"

compose *args:
    @{{compose}}

compose-up:
    @{{compose}} up -w

compose-down:
    @{{compose}} down --rmi local

manage *args:
    @{{manage}} {{args}}
    
migrate *args:
    @{{manage}} migrate {{args}}

minio-alias:
    @{{minio}} alias set myminio http://localhost:9000 minioadmin minioadmin

minio-mb:
    @{{minio}} mb myminio/laboratorio-do-lyc

minio-public-bucket:
    @{{minio}} anonymous set download myminio/laboratorio-do-lyc

minio-setup: minio-alias minio-mb minio-public-bucket
