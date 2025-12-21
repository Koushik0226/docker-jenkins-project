pipeline {
    agent {
        kubernetes {
            inheritFrom 'kaniko'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                container('jnlp') {
                    checkout scm
                }
            }
        }

        stage('Build & Push Image') {
            steps {
                container('kaniko') {
                    sh '''
                      /kaniko/executor \
                        --dockerfile=Dockerfile \
                        --context=/workspace \
                        --destination=docker.io/koushik0226/nginx-demo:latest
                    '''
                }
            }
        }
    }
}
