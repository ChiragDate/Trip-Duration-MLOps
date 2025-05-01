pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yourdockerhub/taxi-duration-api'
        MODEL_DIR = 'models'
        DVC_REMOTE = 'myremote' // Your DVC remote name (can be local)
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
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install dvc
                '''
            }
        }
        
        stage('DVC Setup and Pull') {
            steps {
                sh '''
                    . venv/bin/activate
                    # Initialize DVC if not already initialized
                    if [ ! -d ".dvc" ]; then
                        dvc init
                    fi
                    
                    # Pull latest data/models if they exist
                    dvc pull || echo "No DVC tracked files to pull yet"
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 src/models/train_model.py data/processed
                    
                    # Track the new model with DVC
                    dvc add ${MODEL_DIR}
                    
                    # Commit the changes to Git
                    git config --global user.email "jenkins@example.com"
                    git config --global user.name "Jenkins"
                    git add ${MODEL_DIR}.dvc .gitignore
                    git commit -m "Update model: Jenkins build #${BUILD_NUMBER}" || echo "No changes to commit"
                '''
            }
        }
        
        stage('DVC Push') {
            steps {
                sh '''
                    . venv/bin/activate
                    # Push model to DVC storage
                    dvc push || echo "Nothing to push"
                    
                    # Push .dvc files to Git
                    git push origin HEAD || echo "Nothing to push to Git"
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