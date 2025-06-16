pipeline {
    agent any

    parameters {
        text(name: 'payload', defaultValue: '', description: 'Webhook Payload')
    }

    environment {
        PAYLOAD_DIR = 'payloads'
    }

    stages {

        stage('Prepare Directories') {
            steps {
                sh "mkdir -p ${env.PAYLOAD_DIR}"
            }
        }

        stage('Store Webhook Payload') {
            when {
                expression { return params.payload?.trim() }
            }
            steps {
                script {
                    def timestamp = new Date().format("yyyy-MM-dd_HH-mm-ss")
                    def filename = "${env.PAYLOAD_DIR}/payload_${timestamp}.json"
                    writeFile file: filename, text: params.payload
                    echo "Payload written to ${filename}"

                    sh "find ${env.PAYLOAD_DIR} -name '*.json' -type f -mmin +2880 -delete"
                }
            }
        }

        stage('Setup Virtualenv & Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install pandas openpyxl
                '''
            }
        }

        stage('Aggregate Payloads') {
            steps {
                script {
                    def timestamp = new Date().format("yyyy-MM-dd_HH-mm-ss")
                    sh """
                        source venv/bin/activate
                        python aggregate_payloads.py ${timestamp}
                    """
                }
            }
        }
    }
}
