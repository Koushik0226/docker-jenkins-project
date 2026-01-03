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
    # Start Docker Daemon in background, wait 5s, then keep container running
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
                            checkout scm

                            echo "Logging into Docker Hub..."
                            sh "echo $PASS | docker login -u $USER --password-stdin"

                            echo "Building Docker Image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                            // Builds from the 'App' directory
                            sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./App"

                            echo "Pushing Image to Docker Hub..."
                            sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Trigger Ansible Deployment') {
            steps {
                script {
                    echo "Triggering Remote Ansible Pod..."
                    
                    // Creates the deployment script inside the Ansible pod
                    sh """
                    kubectl exec -n devops deployment/ansible -c ansible -- bash -c 'cat <<EOF > /tmp/deploy-script.sh
ansible-playbook /home/ansible/playbooks/deploy-app.yml --extra-vars "image_name=${IMAGE_NAME} image_tag=${IMAGE_TAG} app_name=${APP_NAME}"
EOF'
                    """

                    // Executes the script
                    sh "kubectl exec -n devops deployment/ansible -c ansible -- bash /tmp/deploy-script.sh"
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! App Deployed."
        }
        failure {
            echo "Pipeline Failed. Check logs."
        }
    }
}