# atacmonitor-data

Backend to collect data from [Open Data](https://romamobilita.it/it/tecnologie/open-data) by RomaMobilita.it. Data is stored in a MongoDB database. The code is divided in the following services:

- `trigger`: AWS Lambda function that schedules and orchestrates the requests to the service
- `palinaList`: AWS Lambda function that provides the list of stations to collect
- `palinaRequest`: AWS Lambda function that sends the request of the waiting times for a certain station
- `gtfsExplore`: exploratory script to detect the stations

## Trigger

When scheduled, this service is

- retrieving the list of stations from `palinaList`
- authenticating to Open Data API service
- invoking `palinaRequest` for every station

To deploy to AWS Lambda:

```
cd trigger
zip function.zip lambda_function.py
aws lambda update-function-code --function-name trigger --zip-file fileb://function.zip
```

## palinaRequest

This service is an API that takes as input an `id_palina`. It sends the request to _romamobilita_ about the current expected arrivals, and it stores the results

To deploy to AWS Lambda ([AWS Ref](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)):

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

To deploy to AWS Lambda:

```
cd palinaList
zip function.zip lambda_function.py
aws lambda update-function-code --function-name palinaList --zip-file fileb://function.zip
```