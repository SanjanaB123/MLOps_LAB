This repo is a small assignment to practice basic Docker image workflows:
build an image, export it as a tar file, and run it locally.

### 1) Build the image
```bash
docker build -t lab1:v1 .
```
### 2) Save the image to a tar file
```bash
docker save lab1:v1 > my_image.tar
```
### 3) Run the image
```bash
docker run lab1:v1
```