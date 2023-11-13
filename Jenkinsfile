def changeBuildCount = 0

pipeline {
    agent any
    stages {
        stage('Set Change Build') {
            script {
                changeBuildCount = currentBuild.changeSets.size()
            }
        }
        stage('Master Branch') {
            when {
                allOf {
                    branch 'master'
                    expression { changeBuildCount > 0 }
                }
            }
            steps {
                sh """
                echo "Building Artifact from Master branch"
                """

                sh """
                echo "${changeBuildCount} commit(s) since last build. Changed Master"
                """
            }
        }

        stage('Develop Branch TEST') {
            when {
                allOf {
                    branch 'dev'
                    expression { changeBuildCount > 0 }
                }
            }
            steps {
                sh """
                echo "Building Artifact from Dev branch"
                """

                sh """
                echo "${changeBuildCount} commit(s) since last build. Changed Dev"
                """
            }
        }
    }
}