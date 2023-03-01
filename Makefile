install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile
	pylint --disable=R,C,W1203,W0702 app.py

# test:
# 	python -m pytest -vv --cov=app test_app.py

build:
	docker build -t rain-prediction:latest .

run:
	docker run -p 8080:8080 rain-prediction

invoke:
	curl http://127.0.0.1:8080/accuracy/Canberra

run-kube:
	kubectl apply -f kube-rain-prediction.yaml

all: install lint

deploy:
	kubectl create deployment knn-predict --image=registry.hub.docker.com/selinaliu/knn-rain-prediction-accuracy
