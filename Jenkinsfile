pipeline {
    agent any

    environment {
        IMAGE_NAME = "ikoushiks/nginx-demo"
        IMAGE_TAG  = "latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/Koushik0226/docker-jenkins-project.git'
            }
        }

        stage('Build & Push Image using Kaniko') {
            steps {
                sh '''
                cat <<EOF | kubectl apply -f -
                apiVersion: batch/v1
                kind: Job
                metadata:
                  name: kaniko-build
                  namespace: devops
                spec:
                  backoffLimit: 0
                  template:
                    spec:
                      restartPolicy: Never
                      containers:
                      - name: kaniko
                        image: gcr.io/kaniko-project/executor:latest
                        args:
                          - "--dockerfile=Dockerfile"
                          - "--context=git://github.com/Koushik0226/docker-jenkins-project.git#refs/heads/main"
                          - "--destination=${IMAGE_NAME}:${IMAGE_TAG}"
                        volumeMounts:
                          - name: docker-config
                            mountPath: /kaniko/.docker
                      volumes:
                        - name: docker-config
                          secret:
                            secretName: dockerhub-secret
                EOF
                '''
            }
        }
    }
}
