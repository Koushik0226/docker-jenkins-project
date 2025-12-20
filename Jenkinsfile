pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "ikoushiks/nginx-demo:latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/Koushik0226/docker-jenkins-project.git'
            }
        }

        stage('Build & Push Image using Kaniko') {
            steps {
                sh '''
                /kaniko/executor \
                  --context $WORKSPACE \
                  --dockerfile Dockerfile.jenkins \
                  --destination $DOCKER_IMAGE
                '''
            }
        }
    }
}
