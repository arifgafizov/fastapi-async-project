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
                    if (changeBuildCount > 0) {
                        echo "${changeBuildCount} commit(s) since last build. Changed Master !!!"

                        sh """
                        echo "Start CI/CD in Master branch."
                        """
                    }
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
                    if (changeBuildCount > 0) {
                        echo "${changeBuildCount} commit(s) since last build. Changed Dev !!!"

                        sh """
                        echo "Start CI/CD in Dev branch."
                        """
                    }
                }
            }
        }

    }
}