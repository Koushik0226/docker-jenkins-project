pipeline {
    agent any 

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        
        IMAGE_NAME = "docker.io/ikoushiks/06-flask-test-app" 
        IMAGE_TAG = "${BUILD_NUMBER}"
        APP_NAME = "06-flask-test-app"
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
                container('image-builder-agent') {
                    script {
                        sh 'sudo dockerd > /var/log/dockerd.log 2>&1 &'
                        sh 'sleep 10'

                        git branch: 'main', url: 'https://github.com/Koushik0226/docker-jenkins-project.git'
                        
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'

                        dir('APP') {
                            sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                            sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Trigger Ansible Deployment') {
            steps {
                script {
                    sh """
                    kubectl exec -n devops deployment/ansible -c ansible -- bash -c 'cat <<EOF > /tmp/deploy-script.sh
ansible-playbook /home/ansible/playbooks/deploy-app.yml --extra-vars "image_name=${IMAGE_NAME} image_tag=${IMAGE_TAG} app_name=${APP_NAME}"
EOF'
                    
                    kubectl exec -n devops deployment/ansible -c ansible -- bash /tmp/deploy-script.sh
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}