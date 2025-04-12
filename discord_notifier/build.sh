#/bin/bash
rm -f deployment_packakages.zip

cd .venv/lib/python3.13/site-packages
zip -r ../../../../deployment_packages.zip .
cd ../../../../
zip deployment_packages.zip src/lambda_function.py
