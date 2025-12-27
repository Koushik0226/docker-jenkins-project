pipeline {
  agent {
    kubernetes {
      label 'kaniko'
      defaultContainer 'kaniko'
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
              --context=$WORKSPACE \
              --destination=ikoushiks/nginx-demo:latest
          '''
        }
      }
    }
  }
}
