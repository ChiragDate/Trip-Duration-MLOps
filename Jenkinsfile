pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yourdockerhub/taxi-duration-api'
        MODEL_DIR = 'models'
        DATA_DIR = 'data'
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
        
        stage('DVC Setup') {
            steps {
                sh '''
                    . venv/bin/activate
                    # Initialize DVC if not already initialized
                    if [ ! -d ".dvc" ]; then
                        dvc init
                    fi
                    
                    # Create data and model directories if they don't exist
                    mkdir -p ${DATA_DIR}/processed
                    mkdir -p ${MODEL_DIR}
                    
                    # Track data directory with DVC if not already tracked
                    if [ ! -f "${DATA_DIR}.dvc" ]; then
                        echo "Setting up initial DVC tracking for data"
                        dvc add ${DATA_DIR}
                    fi
                '''
            }
        }

        stage('Prepare Training Data') {
            steps {
                sh '''
                    . venv/bin/activate
                    # Here you would normally download or prepare your data
                    # For example:
                    # python src/data/make_dataset.py
                    
                    # Create a dummy train.csv if needed for testing
                    if [ ! -f "${DATA_DIR}/processed/train.csv" ]; then
                        echo "Creating dummy training data for testing"
                        echo "feature1,feature2,target" > ${DATA_DIR}/processed/train.csv
                        echo "1,2,3" >> ${DATA_DIR}/processed/train.csv
                        echo "4,5,6" >> ${DATA_DIR}/processed/train.csv
                    fi
                    
                    # Update DVC for data changes
                    dvc add ${DATA_DIR}
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 src/models/train_model.py data/processed
                    
                    # Track the new model with DVC
                    dvc add models
                    
                    # Commit the DVC changes to Git
                    git config --global user.email "jenkins@example.com"
                    git config --global user.name "Jenkins"
                    git add models.dvc .gitignore
                    git commit -m "Update model: Jenkins build #${BUILD_NUMBER}" || echo "No changes to commit"
                '''
            }
        }
        
        stage('DVC Push') {
            when {
                expression { return fileExists('.dvc/config') && sh(script: 'grep -q remote .dvc/config', returnStatus: true) == 0 }
            }
            steps {
                sh '''
                    . venv/bin/activate
                    # Push model to DVC storage if remote is configured
                    dvc push || echo "DVC push failed - remote may not be configured"
                    
                    # Push .dvc files to Git if needed
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