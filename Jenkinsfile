pipeline {
    agent any
    stages {
        stage('Master Branch') {
            when {
                branch 'master'
            }
            steps {
                sh """
                echo "Building Artifact from TEST"
                """

                script {
                    changeCount = currentBuild.changeSets.size()
                }
                sh """
                echo "${changeCount} commit(s) since last build."
                """
            }
        }

        stage('Develop Branch TEST') {
            when {
                branch 'dev'
            }
            steps {
                sh """
                echo "Building Artifact from Dev branch"

                """
                script {
                    def changeCount = 0
                    changeCount = currentBuild.changeSets.size()
                }

                sh """
                echo "${changeCount} commit(s) since last build."
                """
            }
           }
        }
}