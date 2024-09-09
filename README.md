# Simple Pythone DB App 
Frontend used to access and demonstrate the backend functionality.

2. Build docker images:

Each project contains Dockerfile to build docker image.
Please execute following script to build all images.

```
cd app
docker build --rm -t simple-py-web-app .
```

3. Start app
```
docker-compose up -d
```

4. After this prototype system web-application should be available at http://localhost:5000/

# Development
[Visual Studio Code](https://code.visualstudio.com/) can be used as IDE.

Right now `git push origin master` can be used to push changes.\
In the future: [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html#new-merge-request-from-your-local-environment)

Guide for formatting the README: https://www.markdownguide.org/
