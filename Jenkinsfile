pipeline {
  agent {
    kubernetes {
      yamlFile 'jenkins-kaniko.yaml'
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
          --dockerfile=Dockerfile \
          --context=/workspace \
          --destination=docker.io/ikoushiks/nginx-demo:latest
        '''
      }
    }
  }
}
