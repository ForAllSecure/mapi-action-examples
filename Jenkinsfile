pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh '''
                      pip install --user -r requirements.txt 
                   '''
            }
        }
        stage('Scan') {
            steps {
                echo 'Scanning..'
                sh '''
                      FASTAPI_ENV=test coverage run -m uvicorn src.main:app &
                      coverage xml -o coverage.xml
                      curl -Lo mapi https://mayhem4api.forallsecure.com/downloads/cli/latest/linux-musl/mapi && chmod +x mapi
                   '''
                withCredentials([string(credentialsId: 'MAPI_TOKEN', variable: 'MAPI_TOKEN')]) {
                    sh './mapi login ${MAPI_TOKEN}'
                }
                sh '''
                      ./mapi run forallsecure/mapi-action-examples auto "http://localhost:8000/openapi.json" --url "http://localhost:8000/" --junit junit.xml --sarif mapi.sarif --html mapi.html
                   '''
                /* Kill python if it's still running, ignoring any errors */
                sh 'pgrep python3 | xargs kill || true'
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
