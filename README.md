## palinaRequest

This service is an API that takes as input an id_palina. It sends the request to Romamobilita about the current expected arrivals, and it stores the results

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

### test

```
cd palinaRequest
source .test.env.var
python test.py
```

## palinaList

This service is an API that provides the full list of id_palina.

```
cd palinaList
zip function.zip lambda_function.py
aws lambda update-function-code --function-name palinaList --zip-file fileb://function.zip
```