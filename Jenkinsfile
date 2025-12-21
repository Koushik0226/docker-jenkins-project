pipeline {
  agent {
    kubernetes {
      label 'kaniko'
      defaultContainer 'jnlp'
    }
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
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
