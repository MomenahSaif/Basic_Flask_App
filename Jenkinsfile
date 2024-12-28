pipeline {
    agent any
    environment {
        // Set up the virtual environment directory
        VENV_DIR = 'venv'
    }
    stages {
        stage('Clone Repository') {
            steps {
                // Clone the GitHub repository
                git 'https://github.com/MomenahSaif/Basic_Flask_App.git'
            }
        }
        stage('Set up Virtual Environment and Install Dependencies') {
            steps {
                script {
                    // Create a virtual environment
                    sh 'python3 -m venv ${VENV_DIR}'

                    // Activate the virtual environment and install dependencies from requirements.txt
                    sh '''
                    source ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running Tests...'
                // You can add test commands here, for example:
                // sh 'pytest tests'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Here you can add commands for deploying the Flask app
                // For example, if you want to run it on a server:
                // sh 'python app.py'
            }
        }
    }
    post {
        always {
            // Clean up actions after the pipeline runs (e.g., deactivate the virtual environment)
            sh 'deactivate || true'
        }
    }
}
