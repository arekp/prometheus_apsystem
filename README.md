# Prometheus APsystems

Data transformation from [APsystem](https://apsystems.com/) inverters to [Prometheus](https://prometheus.io) format.
Provides power, energy, voltage and temperature metrics.

![Grafana](https://raw.githubusercontent.com/arekp/prometheus_apsystem/master/images/grafana.png)

## Getting Started

These instructions will install and run `prometheus_APsystems` on your system.

### Running with Docker

prometheus_APsystems` is also available as a [Docker](http://docker.com) image
on [Docker Hub](https://hub.docker.com/)
:whale:.

```shell
docker run --rm -d --name prometheus_APsystems --env HOST=http://192.168.1.24 -p 5000:5000/tcp arekp/prometheus_APsystems:latest
```

You can also append extra flags when running with Docker. For example:

```shell
$ docker run --rm --name prometheus_APsystems -p 5000:5000/tcp --env HOST=http://192.168.1.24  arekp/prometheus_APsystems:latest 
```
#### prometheus.yml config

Add this to your
[Prometheus config](https://prometheus.io/docs/prometheus/latest/configuration/configuration)
to start instrumenting APsystems and recording their metrics.

```yaml
global:
  scrape_timeout: 2m

scrape_configs:
- job_name: 'APsystems'
  metrics_path: /metrics
  static_configs:
  - targets:
    - localhost:5000
```

Note if you're running `prometheus` under Docker, you must link the
`prometheus` container to `prometheus_APsystems`. See the steps below for how
this can be done.

#### Trying it out

An example
[Prometheus config](https://prometheus.io/docs/prometheus/latest/configuration/configuration)
has been provided at
[example/prometheus.yml](https://github.com/).
We'll start `prometheus` with this config.


### Instrumenting APsystems with cURL

Once `prometheus_APsystems` has been started, with either Docker 
APsystems can be instrumented with [cURL](https://curl.haxx.se).

```shell
$ curl localhost:5000/metrics
# HELP panele_lifetimegeneration Lifetime Generation
# TYPE panele_lifetimegeneration gauge
panele_lifetimegeneration 4335.2
# HELP panele_generationcurrentday Generation Current of Day
# TYPE panele_generationcurrentday gauge
panele_generationcurrentday 20.56
# HELP panele_LastSystemPower Last System Power
# TYPE panele_LastSystemPower gauge
panele_LastSystemPower 468.0
# HELP panele_Napiecie Napiecie na panelu
# TYPE panele_Napiecie gauge
panele_Napiecie{falownik="801000026000",panel="1"} 237.0
panele_Napiecie{falownik="801000026000",panel="2"} 237.0
panele_Napiecie{falownik="801000026000",panel="3"} 237.0
panele_Napiecie{falownik="801000026000",panel="4"} 237.0
panele_Napiecie{falownik="801000074230",panel="1"} 235.0
panele_Napiecie{falownik="801000074230",panel="2"} 235.0
panele_Napiecie{falownik="801000074230",panel="3"} 235.0
panele_Napiecie{falownik="801000074230",panel="4"} 235.0
panele_Napiecie{falownik="801000030076",panel="1"} 234.0
panele_Napiecie{falownik="801000030076",panel="2"} 234.0
panele_Napiecie{falownik="801000030076",panel="3"} 234.0
panele_Napiecie{falownik="801000030076",panel="4"} 234.0
# HELP panele_Moc moc na panelu
# TYPE panele_Moc gauge
panele_Moc{falownik="801000026000",panel="1"} 32.0
panele_Moc{falownik="801000026000",panel="2"} 41.0
panele_Moc{falownik="801000026000",panel="3"} 0.0
panele_Moc{falownik="801000026000",panel="4"} 45.0
panele_Moc{falownik="801000074230",panel="1"} 36.0
panele_Moc{falownik="801000074230",panel="2"} 43.0
panele_Moc{falownik="801000074230",panel="3"} 46.0
panele_Moc{falownik="801000074230",panel="4"} 46.0
panele_Moc{falownik="801000030076",panel="1"} 43.0
panele_Moc{falownik="801000030076",panel="2"} 43.0
panele_Moc{falownik="801000030076",panel="3"} 47.0
panele_Moc{falownik="801000030076",panel="4"} 46.0
# HELP panele_Temp Temperatura na panelu
# TYPE panele_Temp gauge
panele_Temp{falownik="801000026000"} 39.0
panele_Temp{falownik="801000074230"} 38.0
panele_Temp{falownik="801000030076"} 42.0
# HELP panele_Czestotliwosc Czestotliwosc na panelu
# TYPE panele_Czestotliwosc gauge
panele_Czestotliwosc{falownik="801000026000"} 50.0
panele_Czestotliwosc{falownik="801000074230"} 50.0
panele_Czestotliwosc{falownik="801000030076"} 50.0
```

You can also visit <http://localhost:5000> in your browser to see the same
metrics.

## Getting Started (Development)

These instructions will get you a copy `prometheus_APsystems` up and running on
your local machine for development and testing purposes.

### Prerequisites

* [Python](https://www.python.org)
* [Docker](https://www.docker.com)
* [Pytest](https://pytest.org)

### Running Locally

#### Python

1. Ensure packages listed in
   [requirements.txt](https://github.com/arekp/prometheus_apsystem/blob/master/requirements.txt)
   are installed with `pip`

   ```python
   pip3 install -r requirements.txt
   ```

1. Run `prometheus_APsystems`

   ```python
   python3 app.py
   ```

#### Docker

1. Building image

   ```shell
   docker build -t prometheus_APsystems:latest .
   ```

1. Running

   ```shell
   docker run --rm -d --name prometheus_APsystems -p 5000:5000/tcp --env HOST=http://192.168.1.24 prometheus_APsystems:latest
   ```

### Perform a APsystems

```shell
curl localhost:5000/metrics
```

Or visit <http://localhost:5000/metrics>

### Running Unit Tests

```shell
pytest
```



## Authors

* Arkadiusz Ptak

## License

This product is licensed under the Apache 2.0 license. See [LICENSE](LICENSE)
file for details.

## Acknowledgments

* The Prometheus team <https://prometheus.io>
* Testing in Python team <http://lists.idyll.org/listinfo/testing-in-python>
