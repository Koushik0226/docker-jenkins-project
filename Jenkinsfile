pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/Koushik0226/docker-jenkins-project.git'
            }
        }

        stage('Build') {
            steps {
                echo "Build stage completed successfully"
            }
        }
    }
}
