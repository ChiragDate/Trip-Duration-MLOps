pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yourdockerhub/taxi-duration-api'
        MODEL_DIR = 'models'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip3 install -r requirements.txt
                    pip3 install dvc
                '''
            }
        }

        stage('Pull Data from DVC') {
             steps {
                 sh '''
                     #!/bin/bash
                     . venv/bin/activate
                     dvc pull
                 '''
             }
         }

        stage('Build Features') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 src/features/build_features.py 
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 src/models/train_model.py trip-duration/data/processed/train.csv
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to Kubernetes with Ansible') {
            steps {
                sh 'ansible-playbook ansible/deploy.yml'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
    }
}
