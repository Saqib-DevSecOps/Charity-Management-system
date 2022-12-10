def init(){
  echo "Staarting"
}
def build(){
  echo "Start Builing Docker Image"
  withCredentials([usernamePassword(credentialsId : "Dockerhub" , usernameVariable : "USER", passwordVariable : "PASS")])
				{
					sh "docker build -t 7150148732291/charity:2.0 ."
					sh "echo $PASS | docker login -u $USER --password-stdin"
					sh 'docker push 7150148732291/charity:2.0'
				}	 
}
def test(){
  echo "testiing"
}
def deploy(){
  echo "deploying project with version "
}
return this
