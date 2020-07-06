**1\. install and deploy**  
To install and deploy open `screen` in your terminal and launch the following bash file `deploy.sh`:  
```bash
bash deploy.sh
```  


**2\. API endpoints**  
Here are API endpoints (parameter: `text2translate`):  
current `<host_url> = http://ec2-35-180-2-236.eu-west-3.compute.amazonaws.com`  
To translate FR to EN: `<host_url>:8080/fr2en`  
To translate EN to FR: `<host_url>:8080/en2fr`  
To translate DE to EN: `<host_url>:8080/de2en`  
To translate EN to DE: `<host_url>:8080/en2en`  
To translate FR to DE: `<host_url>:8080/fr2de`  
To translate DE to FR: `<host_url>:8080/de2fr`  



**3\. Example of usage in python code**
You can find and example of to use it in python code in this file [example_request.py](https://gitlab.com/PPTECH-platform/datascience/translator/blob/master/examples/example_request.py)
