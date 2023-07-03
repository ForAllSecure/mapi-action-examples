// First job
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh '''
                      pip install -r requirements.txt 
                   '''
            }
        }
        stage('Start API') {
            steps {
                echo 'Building..'
                sh '''
                      FASTAPI_ENV=test python3 -m coverage run -m uvicorn src.main:app &
                   '''
            }
        }
        stage('Scan') {
            steps {
                script {
                    try {
                        echo 'Scanning..'
                        sh '''
                              curl -Lo mapi ${MAYHEM_URL}/cli/mapi/linux-musl/latest/mapi && chmod +x mapi
                           '''
                        withCredentials([string(credentialsId: 'MAPI_TOKEN', variable: 'MAPI_TOKEN')]) {
                            sh '''
                                    ./mapi login ${MAPI_TOKEN}
                                    ./mapi run forallsecure/mapi-action-examples/fastapi auto "http://localhost:8000/openapi.json" --url "http://localhost:8000/" --junit junit.xml --sarif mapi.sarif --html mapi.html
                               '''
                        }
                    } finally {
                        /* Kill python if it's still running, ignoring any errors */
                        sh 'pgrep python3 | xargs kill || true'

                        /* Generate coverage report */
                        sh 'python3 -m coverage xml -o coverage.xml'
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Archive and Code coverage....'
            archiveArtifacts artifacts: 'junit.xml, mapi.sarif, mapi.html, coverage.xml',
                allowEmptyArchive: true,
                fingerprint: true,
                onlyIfSuccessful: false
            junit 'junit.xml'
            cobertura coberturaReportFile: 'coverage.xml', onlyStable: 'false'
        }
    }
}
