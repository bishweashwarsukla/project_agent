# project_agent

---------------------------------------------------------------------------------------------------------------------------------
How to setup environment ?
steps
1. python - m venv <envname>
2. kill terminal and restart it again
3. pip install --upgrade pip setuptools
4. source venv activate
5. pip3 install -r requirements.txt
---------------------------------------------------------------------------------------------------------------------------------

- agent to get good news and bad news about a particular stock and agent to tell about news - in market about market conditions , bullish , bearish , and stocks in news
- web app for multiple users hence we are using vectoredb ( we are creating vectordb to store embeddings and cache the data so that we can use as many times as we want )
- scheduled run every day for updating vectore db

---------------------------------------------------------------------------------------------------------------------------------

optional -> web serach api add as a node
1) web app -> input and output
2) every day 8 am -> query web and updated vd automatically -> github actions/airflow/anyother method ( custom function)
3) docker image 
4) github actions for docker image building on push to prod
5) github secrets ( keep env file there)
6) langsmith ( optional)
7) how much FII and DII buy/sold every day - add this as a feature 
8) in webapp, make it in for loop such till user hit exit, it will show result 
9) add relevant questions as suggestion to user so he/she can check out those
10) add yahoo finance api


![graph image](/project_agent/input/images/graph.jpg)

![graph image 2](/project_agent/input/images/graph2.jpg)

<img src="/project_agent/input/images/graph-1.png" width="128"/>
<img src="/project_agent/input/images/graph-2.png" width="128"/>

how to run :
- sudo systemctl start docker / start docker desktop if in ubuntu
- docker pull {image name from docker hub}
- docker run - p 5000:5000 {image name from docker hub}

[![CI/CD for Dockerized App](https://github.com/bishweashwarsukla/project_agent/actions/workflows/ci-cd.yml/badge.svg?branch=prod)](https://github.com/bishweashwarsukla/project_agent/actions/workflows/ci-cd.yml)

