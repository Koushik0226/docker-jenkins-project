pipeline {
    agent any

    environment {
        // Name your image
        IMAGE_NAME = "my-python-flask-app"
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls code from your git repo (Automatic in most Jenkins setups)
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    // CRITICAL: We point to the ./App directory for the build context
                    // This command says: "Look in ./App for the Dockerfile and code"
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ./App"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running Tests...'
                    // Example: Run a temporary container to check if it starts
                    sh "docker run -d -p 5000:5000 --name test-container ${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "sleep 5" // Give it a moment to boot
                    sh "curl http://localhost:5000" // Check if it responds
                }
            }
            post {
                always {
                    // Clean up the test container
                    sh "docker rm -f test-container"
                }
            }
        }

        stage('Push/Deploy') {
            steps {
                echo 'Placeholder: Push to Registry or Deploy to Server'
                // sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }
    }
}