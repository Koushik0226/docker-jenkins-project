pipeline {
    // Global agent is 'any'. This runs on the Jenkins Master by default,
    // which allows us to use 'kubectl' in the deployment stage (solving the error on PDF Page 68).
    agent any 

    environment {
        // YOUR DETAILS ADDED HERE
        DOCKER_IMAGE = "ikoushiks/docker-jenkins-project" 
        APP_NAME = "docker-jenkins-project"
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        // Ensure this matches the ID you created in Jenkins (PDF Page 44)
        DOCKER_CRED_ID = "dockerhub-cred" 
    }

    stages {
        // STAGE 1: Build & Push (Runs inside the dynamic K8s Agent)
        stage('Docker Build & Push') {
            agent {
                kubernetes {
                    // We use the RHEL9 image as specified in the PDF (Page 67)
                    // The standard Alpine image causes iptables errors.
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
                            echo "Building Docker Image..."
                            // ⚠️ IMPORTANT: If your Dockerfile is inside a folder named 'APP' (like in the PDF),
                            // uncomment the line below. Otherwise, use the standard build command.
                            // sh "cd APP/ && docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                            
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

        // STAGE 2: Deploy (Runs on Jenkins Master)
        stage('Trigger Ansible Deployment') {
            steps {
                script {
                    echo "Triggering Ansible Pod to deploy..."
                    // This runs on the Master node, so 'kubectl' works here.
                    // It passes YOUR specific image/app variables to the Ansible playbook.
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