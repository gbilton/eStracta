run: 
	flask --app app.main run --debug
restart:
	docker compose down && docker compose up -d --build
freeze:
	pip freeze > app/requirements.txt