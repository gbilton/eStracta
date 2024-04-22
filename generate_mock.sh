#!/bin/bash

# URL do servidor
url="http://localhost:5000/companies"

# Loop sobre cada linha do arquivo CSV
while IFS=',' read -r cnae cnpj nome_razao nome_fantasia; do
    # Formatando os dados em JSON
    json="{\"cnpj\": \"$cnpj\", \"nome_razao\": \"$nome_razao\", \"nome_fantasia\": \"$nome_fantasia\", \"cnae\": \"$cnae\"}"

    # Enviar os dados para o servidor usando curl
    curl -X 'POST' \
        "$url" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "$json"
done < mock.csv

