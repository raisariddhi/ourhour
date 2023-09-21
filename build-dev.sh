fs sa . system:anyuser rlidwka
find . -type d -exec fs sa {} system:anyuser rlidwka \;
docker compose -f docker-compose-dev.yml up --build;
