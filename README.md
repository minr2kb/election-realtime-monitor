# 선거 실시간 모니터링툴

## Quick Start

### Webdriver Installation

> 크롤링을 위해 사용하게될 Selenium 라이브러리의 사용을 위해 chromedriver가 필요합니다. 설치된 크롬 버젼을 확인해주시고 [이 곳](https://chromedriver.chromium.org/downloads) 에서 운영체제에 맞는 드라이버를 다운 받아 루트 디렉토리에 위치시켜주세요.

## Virtual Env.

> 혹시 모를 라이브러리의 버젼 충돌을 없애기 위해 가상환경을 사용합니다

### mac

```bash
# Create the env
python3 -m venv venv

# Activate the env
. venv/bin/activate

# install packages
pip3 install -r requirements.txt
```

```python
# excute the crawler
python3 crawler.py
```

### windows

```bash
# Create the env
py -3 -m venv venv

# Activate the env
venv\Scripts\activate

# install packages
pip install -r requirements.txt
```

```python
# excute the crawler
python crawler.py
```
