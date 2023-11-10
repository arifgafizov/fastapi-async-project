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

                echo "${changeCount} commit(s) since last buid."
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
                    changeCount = currentBuild.changeSets.size()
                }

                echo "${changeCount} commit(s) since last buid."
            }
           }
        }
}