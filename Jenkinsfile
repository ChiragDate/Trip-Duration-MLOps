pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.10.12'
        DVC_MODELS_DIR = "/home/mohit-marfatia/SPE/train-data"
        VENV_PATH = "${WORKSPACE}/trip_duration_venv"
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                sh '''
                    # Create virtual environment in workspace for proper permissions
                    python3 -m venv ${VENV_PATH}
                    
                    # Make sure activation script is executable
                    chmod +x ${VENV_PATH}/bin/activate
                    
                    # Activate virtual environment and install dependencies
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install dvc
                '''
            }
        }
        
        stage('Fix DVC Permissions') {
            steps {
                // This requires that the Jenkins user has sudo access or that someone runs this manually once
                sh '''
                    # Make the DVC data directory accessible to Jenkins
                    # Option 1: If you have sudo access in Jenkins:
                    # sudo chmod -R 755 ${DVC_MODELS_DIR}
                    
                    # Option 2: Copy the data to a location Jenkins can access
                    mkdir -p ${WORKSPACE}/dvc_cache
                    
                    # Configure DVC to use the workspace cache
                    . ${VENV_PATH}/bin/activate
                    dvc cache dir ${WORKSPACE}/dvc_cache
                    
                    # You might need to initialize DVC first
                    if [ ! -d .dvc ]; then
                        dvc init
                    fi
                '''
            }
        }
        
        stage('Pull Models') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    dvc --version
                    
                    # Create a new remote that points to a location Jenkins can access
                    dvc remote add -d workspace-remote ${WORKSPACE}/dvc_cache
                    
                    # Try pulling from the new remote
                    dvc pull -v
                    
                    # If the above fails, you may need to manually copy the model files
                    mkdir -p models data
                '''
            }
        }
    }
    
    post {
        always {
            echo "Pipeline completed"
        }
    }
}