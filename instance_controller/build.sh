#/bin/bash
rm -f deployment_packakages.zip

zip -r deployment_packakages.zip .venv/lib/python3.13/site-packages
zip deployment_packakages.zip lambda_function.py
