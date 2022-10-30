
# Manga Downloader

As the name says, its a project that downloads manga.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
git
python3.9
```

### Installing

First of all you need to clone the repository:

```bash
git clone git@github.com:christianfds/manga_downloader.git
```

Then install the dependencies in a virtual environment:

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

With this you are ready to download any manga available on the providers:

```bash
python manga_downloader.py -m "One Piece" -o "./out/"
```

### Building and running with Docker image

To run the application without installing the dependencies in your machine, you can execute the CLI with docker, following the steps bellow:

> If you don't have Docker installed, please see how [install here](https://docs.docker.com/engine/install/).

```bash
docker build -t manga-downloader-cli .

```

Now we can run our image, with the command bellow:

```bash
docker run -it --name md-cli --rm  manga-downloader-cli
```

At this point, we can start our CLI with the same commands we would use on the host, e.g.:

```bash
appuser@281f592323c4:/app$ python manga_downloader.py -m "One Piece" -o "./out/"
```

Another alternative to run the CLI, is using Docker Compose, this make the things easy. And at this point, the only thing we need is run the following command:

```bash
docker-compose up -d flaresolverr
docker-compose run --rm cli

```

It will build the docker image, run it and also creates a volume folder in app root, to save the download content in the folder `./out` in root of our application.

### FlareSolverr
Its possible to use [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) to solve most issues with cloudflare, the best way to do it is by using the Docker Compose, but if you want its possible to set the environment variable `FLARESOLVERR_URL`

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
