## palinaRequest

[AWS Ref](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

Create the virtual env and install dependencies:

```
cd palinaRequest
python3 -m venv palinaRequest
source palinaRequest/bin/activate
pip install -r requirements.txt
deactivate
```

Create zip file and upload to aws:

```
cd palinaRequest/lib/python3.7/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py arrival.py
aws lambda update-function-code --function-name palinaRequest --zip-file fileb://function.zip
```