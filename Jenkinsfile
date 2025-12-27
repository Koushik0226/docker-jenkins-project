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
        sh '''
        /kaniko/executor \
          --context=$WORKSPACE \
          --dockerfile=$WORKSPACE/Dockerfile \
          --destination=ikoushiks/nginx-demo:latest
        '''
      }
    }
  }
}
