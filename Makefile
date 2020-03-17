clean:
	rm -f html_output/*.html
	rm -f html_output/address_audit_report/*.html
	rm -f html_output/address_report/*.html
	rm -f html_output/mab_report/*.html
	rm -f html_output/minting_rewards_report/*.html

reports:
	python index.py
	python address_audit_report.py
	python address_report.py
	python mab_report.py
	python minting_rewards_report.py
