def changeBuildCount = 0

pipeline {
    agent any
    stages {
        stage('Master Branch') {
            when {branch 'master'}
            steps {
                sh """
                echo "Building Artifact from Master branch"
                """

                script {
                    changeBuildCount = currentBuild.changeSets.size()
                }

                when {
                    expression { changeBuildCount > 0 }
                }
                steps {
                    sh """
                    echo "${changeBuildCount} commit(s) since last build. Changed Master"
                    """
                }
            }
        }

        stage('Develop Branch TEST') {
            when {branch 'dev'}
            steps {
                sh """
                echo "Building Artifact from Dev branch"
                """

                script {
                    changeBuildCount = currentBuild.changeSets.size()
                }

                when {
                    expression { changeBuildCount > 0 }
                }
                steps {
                    sh """
                    echo "${changeBuildCount} commit(s) since last build. Changed Dev"
                    """
                }
            }
        }
    }
}