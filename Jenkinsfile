pipeline {
  agent {
    kubernetes {
      label 'kaniko'
      defaultContainer 'jnlp'

      yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: slave
spec:
  serviceAccountName: jenkins
  restartPolicy: Never

  volumes:
  - name: workspace-volume
    emptyDir: {}
  - name: docker-config
    secret:
      secretName: dockerhub-secret

  containers:
  - name: jnlp
    image: jenkins/inbound-agent:4.13.3-1
    workingDir: /home/jenkins/agent
    volumeMounts:
    - name: workspace-volume
      mountPath: /home/jenkins/agent

  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - /busybox/sh
    - -c
    args:
    - cat
    tty: true
    volumeMounts:
    - name: workspace-volume
      mountPath: /workspace
    - name: docker-config
      mountPath: /kaniko/.docker
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
            --dockerfile=Dockerfile \
            --context=/workspace \
            --destination=docker.io/koushik0226/nginx-demo:latest
          '''
        }
      }
    }
  }
}
