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
                script {
                    sh "mkdir -p ${env.PAYLOAD_DIR}"
                }
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

                    // Clean payload files older than 48 hours (2880 minutes)
                    sh """
                        find ${env.PAYLOAD_DIR} -name "*.json" -type f -mmin +2880 -delete
                    """
                }
            }
        }

        stage('Aggregate Payloads (last 24h)') {
            steps {
                script {
                    def timestamp = new Date().format("yyyy-MM-dd_HH-mm-ss")

                    // Clean previous Excel files before aggregation
                    sh "rm -f slave*.xlsx"

                    // Run aggregation script
                    sh "python3 aggregate_payloads.py ${timestamp}"
                }
            }
        }
    }
}
