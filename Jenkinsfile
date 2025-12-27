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
  - name: jnlp
    image: jenkins/inbound-agent:latest
    args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
    volumeMounts:
    - name: workspace
      mountPath: /home/jenkins/agent

  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command:
    - /busybox/cat
    tty: true
    volumeMounts:
    - name: workspace
      mountPath: /workspace
    - name: docker-config
      mountPath: /kaniko/.docker

  volumes:
  - name: workspace
    emptyDir: {}

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
              --context=/workspace \
              --destination=ikoushiks/nginx-demo:latest
          '''
        }
      }
    }
  }
}
