pipeline {
  agent {
    kubernetes {
      label 'kaniko'
      defaultContainer 'kaniko'
      yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker
    - name: workspace
      mountPath: /workspace

  volumes:
  - name: docker-config
    secret:
      secretName: dockerhub-secret
      items:
      - key: .dockerconfigjson
        path: config.json

  - name: workspace
    emptyDir: {}
"""
    }
  }

  stages {

    stage('Checkout') {
      steps {
        container('kaniko') {
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
            --destination=docker.io/ikoushiks/nginx-demo:latest
          '''
        }
      }
    }
  }
}
