// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_name = credentials('wp_name')
        server_host = credentials('wp_host')
        ssh_key = credentials('wp_devops')
    }

    stages {
        stage('Ssh to connect bigelow server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host
                    
                }
            }
        }
        stage('Download latest release and create enviroment') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpoinsAdmin
                        if [ ! -d admin_WP ]; then
                            mkdir ./admin_WP
                        fi
                        cd /var/www/waterpoinsAdmin/admin_WP
                        rm -rf env
                        rm -rf src
                        kill -9 $(lsof -t -i:5002)
                        curl -LOk https://github.com/CIAT-DAPA/lswms_admin/releases/latest/download/releaseADMIN.zip
                        unzip -o releaseADMIN.zip
                        rm -fr releaseADMIN.zip
                        python3 -m venv env
                    """
                }
            }
        }
        stage(' activate enviroment and install requirements') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpoinsAdmin/admin_WP
                        source env/bin/activate
                        cd src
                        pip install -r requirements.txt
                    """
                }
            }
        }
        stage('Init admin') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        cd /var/www/waterpoinsAdmin/admin_WP
                        source env/bin/activate
                        cd src
                        export DEBUG=False
                        export WP_ADMIN_PORT=5002
                        export CONNECTION_DB=mongodb://localhost:27017/waterpoints
                        export HOST=0.0.0.0
                        export WP_ADMIN_USER=ethwaterpoints
                        export WP_ADMIN_PASSWORD=EthWP151123
                        nohup python3 app.py > log.txt 2>&1 &
                    """
                }
            }
        }       
    }
    
    post {
        failure {
            script {
                echo 'fail'
            }
        }

        success {
            script {
                echo 'everything went very well, admin in production'
            }
        }
    }
 
}
