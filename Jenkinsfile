pipeline {
  agent {
    kubernetes {
      label 'kaniko'
      defaultContainer 'kaniko'

      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:4.13.3-1
    workingDir: /home/jenkins/agent
    tty: true

  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
      - /busybox/cat
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
              --context=$(pwd) \
              --destination=docker.io/koushik0226/nginx-demo:latest
          '''
        }
      }
    }
  }
}
