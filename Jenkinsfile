pipeline {
  agent {
    kubernetes {
      inheritFrom 'kaniko'
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
            --context=/var/jenkins_home/workspace/k8s-cicd-pipeline \
            --destination=docker.io/koushik0226/nginx-demo:latest
          '''
        }
      }
    }
  }
}
