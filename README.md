# 선거 실시간 모니터링툴

## Quick Start

### Webdriver Installation

크롤링을 위해 사용하게될 Selenium 라이브러리의 사용을 위해 chromedriver가 필요합니다. 설치된 크롬 버젼을 확인해주시고 [이 곳](https://chromedriver.chromium.org/downloads) 에서 운영체제에 맞는 드라이버를 다운 받아 루트 디렉토리에 위치시켜주세요.

> mac의 경우 처음 드라이버 실행시 "'chromedriver'은(는) Apple에서 악성 소프트웨어가 있는지 확인할 수 없기 때문에 열 수 없습니다." 오류가 뜹니다. 그러면 `시스템 환경 설정 > 보안 및 개인 정보 보호` 에서 가장 아래의 "확인 없이 허용"을 눌러주신 후 재실행 해주세요!

## Virtual Env.

혹시 모를 라이브러리의 버젼 충돌을 없애기 위해 가상환경을 사용합니다

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
python3 server.py
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
python server.py
```
