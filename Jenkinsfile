pipeline {
    agent any 

    environment {
        DOCKER_IMAGE = "ikoushiks/docker-jenkins-project" 
        APP_NAME = "docker-jenkins-project"
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        DOCKER_CRED_ID = "dockerhub-cred" 
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
    command:
    - cat
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
                withCredentials([usernamePassword(credentialsId: DOCKER_CRED_ID, passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    container('image-builder-agent') {
                        script {
                            echo "Starting Docker Daemon..."
                            sh 'sudo dockerd > /dev/null 2>&1 &'
                            
                            sh 'sleep 10'
                            
                            echo "Building Docker Image..."
                            sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                            
                            echo "Login to Docker Hub..."
                            sh "echo $PASS | docker login -u $USER --password-stdin"
                            
                            echo "Pushing Image..."
                            sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Trigger Ansible Deployment') {
            steps {
                script {
                    echo "Triggering Ansible Pod to deploy..."
                    sh """
                    kubectl exec -n devops deployment/ansible -c ansible -- bash -c 'cat <<EOF > /tmp/deploy-script.sh
ansible-playbook /home/ansible/playbooks/deploy-app.yml --extra-vars "image_name=${DOCKER_IMAGE} image_tag=${IMAGE_TAG} app_name=${APP_NAME}"
EOF'
                    kubectl exec -n devops deployment/ansible -c ansible -- bash /tmp/deploy-script.sh
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}