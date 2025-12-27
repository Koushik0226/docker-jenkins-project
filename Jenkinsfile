pipeline {
  agent {
    kubernetes {
      yamlFile 'jenkins-kaniko-pod.yaml'
      defaultContainer 'kaniko'
    }
  }

  stages {
    stage('Build & Push Image') {
      steps {
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
