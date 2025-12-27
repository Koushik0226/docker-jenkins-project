pipeline {
  agent {
    kubernetes {
      label 'kaniko-agent'
      defaultContainer 'kaniko'
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
  - name: jnlp
    image: jenkins/inbound-agent:latest
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
        sh '''
          /kaniko/executor \
            --dockerfile=Dockerfile \
            --context=. \
            --destination=docker.io/ikoushiks/nginx-demo:latest
        '''
      }
    }
  }
}
