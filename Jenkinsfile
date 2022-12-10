pipeline{
agent any 
	stages{
		
		stage("INIT")
		{
			steps {
				script {
				scr = load "script.groovy"
				scr.init()
				}
			}
		}
		stage("BUIld"){
		
			when {
				expression{
					env.BRANCH_NAME == 'main'
				}
			}
			steps{
				script{
				scr.build()
				}

			}
			}
		stage("TEST") {
			steps { 
				script {
					scr.test()
				}
			}
		}
		stage("Deployed"){
			steps {
				script {
					scr.deploy()
				}
			}
		}
}
}
