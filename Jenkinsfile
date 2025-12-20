pipeline {
  agent {
    kubernetes {
      label 'jenkins'
      defaultContainer 'jnlp'
    }
  }

  environment {
    IMAGE_NAME = "ikoushiks/nginx-demo"
    IMAGE_TAG  = "latest"
  }

  stages {

    stage('Checkout Code') {
      steps {
        checkout scm
      }
    }

    stage('Build & Push Image (Kaniko)') {
      steps {
        container('kaniko') {
          sh '''
          /kaniko/executor \
            --dockerfile=Dockerfile \
            --context=/workspace \
            --destination=${IMAGE_NAME}:${IMAGE_TAG}
          '''
        }
      }
    }
  }
}
