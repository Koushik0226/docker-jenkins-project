pipeline {
  agent {
    kubernetes {
      label 'kaniko-agent'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  volumes:
  - name: docker-config
    secret:
      secretName: dockerhub-secret
"""
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
            --context $WORKSPACE \
            --dockerfile Dockerfile \
            --destination docker.io/ikoushiks/nginx-demo:latest
          '''
        }
      }
    }
  }
}
