pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "ikoushiks" 
        APP_NAME = "docker-jenkins-project" 
        IMAGE_NAME = "${DOCKERHUB_USER}/${APP_NAME}"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Docker Build & Push') {
            agent {
                kubernetes {
                    yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: image-builder-agent
spec:
  containers:
  - name: image-builder-agent
    image: docker.io/sayantan2k21/image-builder-k8s-agent:rhel9
    securityContext:
      privileged: true
    # FIX: Start Docker Daemon in background, wait 5s, then keep container running
    command:
    - /bin/sh
    - -c
    - "sudo dockerd --host=unix:///var/run/docker.sock & sleep 5 && cat"
    tty: true
    volumeMounts:
    - name: docker-graph-storage
      mountPath: /var/lib/docker
  volumes:
  - name: docker-graph-storage
    emptyDir: {}
"""
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    container('image-builder-agent') {
                        script {
                            echo "Checkout Source Code..."
                            dir('App') {
                                echo "Current Directory: ${pwd()}"
                                
                                echo "Building Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}"
                                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                                
                                echo "Login to DockerHub..."
                                sh "echo $PASS | docker login -u $USER --password-stdin"
                                
                                echo "Pushing Image..."
                                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                            }
                        }
                    }
                }
            }
        }
    }
}