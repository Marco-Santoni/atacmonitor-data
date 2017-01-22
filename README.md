# atacmonitor-data

Application that gets data to [atacmonitor](http://atacmonitor.com/).

## Setup

The app runs under the Python version specified under `runtime.txt`.

Install all packages.

```bash
pip install -r requirements.txt
```

Create a development PostgreSQL database.

```bash
createdb atacmonitor_development
```

and run the SQL migrations under `migrations`.

## Collect data

Store waiting times for stops (`paline`).

```bash
python data_collector.py
```

## Update stop list

Download and unzip [Rete del trasporto pubblico](https://romamobilita.it/node/316). Take the `stops.txt` file and save it under `data`.

Then

```bash
python update_paline.py
```
