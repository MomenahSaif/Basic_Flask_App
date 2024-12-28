pipeline {
    agent any
    environment {
        // Set up the virtual environment directory
        VENV_DIR = 'venv'
        // Define the target directory for deployment
        TARGET_DIR = '/path/to/target/directory'
        // Define the name of the package for build step (e.g., a .tar.gz file)
        PACKAGE_NAME = 'flask_app_package.tar.gz'
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
        stage('Build') {
            steps {
                echo 'Building the app...'
                script {
                    // Package the app (e.g., create a tarball or zip file)
                    sh '''
                    tar -czf ${PACKAGE_NAME} *  # Adjust this command as needed for your app structure
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    // Run tests using pytest
                    sh '''
                    source ${VENV_DIR}/bin/activate
                    pytest --maxfail=1 --disable-warnings -q  # Adjust pytest options as needed
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the app...'
                script {
                    // Copy the necessary files to the target directory
                    sh '''
                    cp -r * ${TARGET_DIR}  # Adjust this command as needed for your deployment process
                    '''
                }
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
