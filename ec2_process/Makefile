all:

clean: 
	rm -f *pyc .*swp

rem: clean
	rm -f debug_log

copy_from_instance:
	scp -r -i ~/Downloads/project_ec2_instance.pem ubuntu@ec2-54-172-54-162.compute-1.amazonaws.com:~/ec2_process/ ../; make rem

push:
	ssh -i ~/Downloads/project_ec2_instance.pem ubuntu@ec2-54-172-54-162.compute-1.amazonaws.com 'rm -rf ec2_process'
	scp -r -i ~/Downloads/project_ec2_instance.pem ../ec2_process/ ubuntu@ec2-54-172-54-162.compute-1.amazonaws.com:~
	ssh -i ~/Downloads/project_ec2_instance.pem ubuntu@ec2-54-172-54-162.compute-1.amazonaws.com 'cd ec2_process; make rem'

