clean:
	rm -f html_output/*.html
	rm -f html_output/address_audit_report/*.html
	rm -f html_output/address_report/*.html
	rm -f html_output/supernode_report/*.html
	rm -rf html_output/minting_reward_report
	mkdir html_output/minting_reward_report
	cp html_output/supernode_report/.gitignore html_output/minting_reward_report/

reports:
	python index.py
	python address_audit_report.py
	python address_report.py
	python supernode_report.py
	python minting_reward_report.py
