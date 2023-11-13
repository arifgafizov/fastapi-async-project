pipeline {
    agent any
    stages {
        stage('Master Branch') {
            when {branch 'master'}
            steps {
                sh """
                echo "Building Artifact from Master branch"
                """

                sh """
                    echo "Start CI/CD in Master branch. changeBuildCount"
                """

            }
        }

        stage('Develop Branch') {
            when {branch 'dev'}
            steps {
                sh """
                echo "Building Artifact from Dev branch"
                """

                sh """
                    echo "Start CI/CD in Dev branch, without changeBuildCount"
                """
            }
        }

    }
}