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
                    sh """
                    if changeBuildCount > 0
                    then
                        echo "${changeBuildCount} commit(s) since last build. Changed Master"
                    fi
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
                    sh """
                    if changeBuildCount > 0
                    then
                        echo "${changeBuildCount} commit(s) since last build. Changed Dev"
                    fi
                    """
                }
            }
        }

    }
}