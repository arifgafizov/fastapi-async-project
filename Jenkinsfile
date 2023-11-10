def changeBuildCount = 0

pipeline {
    agent any
    stages {
        stage('Master Branch') {
            when {
                allOf {
                    branch 'master'
                    changeBuildCount > 0
                }
            }
            steps {
                sh """
                echo "Building Artifact from TEST"
                """

                script {
                    changeBuildCount = currentBuild.changeSets.size()
                }
                sh """
                echo "${changeBuildCount} commit(s) since last build. Changed"
                """
            }
        }

        stage('Develop Branch TEST') {
            when {
                allOf {
                    branch 'dev'
                    changeBuildCount > 0
                }
            }
            steps {
                sh """
                echo "Building Artifact from Dev branch"

                """
                script {
                    changeBuildCount = currentBuild.changeSets.size()
                }

                sh """
                echo "${changeBuildCount} commit(s) since last build. Changed"
                """
            }
           }
        }
}