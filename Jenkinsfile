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
        stage('Scan') {
            steps {
                script {
                    try {
                        echo 'Scanning..'
                        sh '''
                              FASTAPI_ENV=test python3 -m coverage run -m uvicorn src.main:app &
                              curl -Lo mapi https://mayhem4api.forallsecure.com/downloads/cli/latest/linux-musl/mapi && chmod +x mapi
                           '''
                        withCredentials([string(credentialsId: 'MAPI_TOKEN', variable: 'MAPI_TOKEN')]) {
                            sh '''
                                    ./mapi login ${MAPI_TOKEN}
                               '''
                        }
                        sh '''
                                ./mapi run forallsecure/mapi-action-examples auto "http://localhost:8000/openapi.json" --url "http://localhost:8000/" --junit junit.xml --sarif mapi.sarif --html mapi.html
                           '''

                        error('This build is intentionally marked as failed for testing.')

                    } catch(Exception e) {
                        echo 'Exception occurred: ' + e.getMessage()
                        currentBuild.result = 'FAILURE'
                    } finally {
                        /* Kill python if it's still running, ignoring any errors */
                        sh 'pgrep python3 | xargs kill || true'

                        /* Generate coverage report */
                        sh 'python3 -m coverage xml -o coverage.xml'
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
                    cobertura coberturaReportFile: 'coverage.xml'
                    recordIssues(
                        enabledForFailure: true,
                        tool: sarif(pattern: 'mapi.sarif')
                    )
                }
            }
        }
    }
}
