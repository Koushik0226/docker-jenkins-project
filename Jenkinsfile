pipeline {
    agent any

    environment {
        IMAGE_NAME = "ikoushiks/nginx-demo"
        IMAGE_TAG  = "latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/Koushik0226/docker-jenkins-project'
            }
        }

        stage('Build & Push Image (Kaniko)') {
            steps {
                container('kaniko') {
                    sh '''
                    /kaniko/executor \
                      --dockerfile=Dockerfile \
                      --context=/var/jenkins_home/workspace/${JOB_NAME} \
                      --destination=${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }
    }
}
