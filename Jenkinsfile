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
        
        stage('Initialize DVC') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    
                    # Initialize DVC if not already done
                    if [ ! -d .dvc ]; then
                        dvc init
                    fi
                    
                    # Configure DVC to use local directory for models
                    dvc config core.no_scm true
                    
                    # Add the external data directory as a remote (if not already added)
                    dvc remote add -d local-models ${DVC_MODELS_DIR}
                    
                    # Make sure the directories exist
                    mkdir -p models data
                '''
            }
        }
        
        stage('Pull Models') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    dvc --version
                    
                    # First check if models and data are being tracked by DVC
                    if [ ! -f models.dvc ] && [ ! -f data.dvc ]; then
                        echo "Models and data not tracked yet, adding to DVC"
                        # Add models and data directories to DVC tracking if they exist
                        [ -d models ] && dvc add models
                        [ -d data ] && dvc add data
                    fi
                    
                    # Pull models from DVC tracking
                    dvc pull -v  # Added -v for verbose output to debug
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