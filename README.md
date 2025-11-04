# Safe Notes

A bare-bones note taking application written with Python and Flask.

## How to Run

Ensure Docker is installed on your system.

Run the following commands to build and run the `Dockerfile`:

```bash
docker build . -t safenotes
docker run -p 8080:8080 safenotes
```

Visit the site at http://localhost:8080/

## How to Test

Run the following commands to execute unit tests for this app:

```bash
docker build . -t safenotes-test -f .sadguard/Dockerfile
docker run safenotes-test
```

