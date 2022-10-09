
# Manga Downloader
As the name says, its a project that downloads manga.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
```
git
python3.9
poetry
```
### Installing
First of all you need to clone the repository:
```bash
git clone git@github.com:christianfds/manga_downloader.git
```
Then install the dependencies in a virtual environment:
```bash
poetry install
```

With this you are ready to download any manga available on the providers:
```bash
python manga_downloader.py -m "One Piece" -o "./out/"
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
