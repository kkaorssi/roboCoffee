# Coffee Drip Robot System
## Overview
이 프로젝트는 안드로이드 태블릿 앱을 통해 주문을 받아 로봇이 커피 드립을 자동으로 수행하는 시스템입니다.
백엔드는 Django와 Django REST Framework (DRF)를 사용하여 주문, 레시피, 북마크 데이터를 관리하고 API를 제공합니다.
로봇은 HTTP 요청을 통해 주문 정보를 가져와 커피 드립 과정을 수행합니다.

## Run Image
<img src="https://github.com/user-attachments/assets/4804022c-d3d9-4e69-890f-a7374abf02f0">

### Key Components::
- Django + DRF 백엔드: SQLite에 저장된 주문, 레시피, 북마크 데이터를 관리하는 API를 제공.
- 안드로이드 태블릿 앱: 커피 주문을 위한 사용자 인터페이스.
- 로봇: 실제 커피 드립을 수행. Fairino 3 협동 로봇 사용.
- 컴퓨터 비전 (Yolov8): 커피 드립 과정에서 필요한 인간 개입이 완료되었는지 확인.

## System Workflow
### 1. Order Placement
- 사용자가 안드로이드 태블릿 앱을 통해 커피 주문을 합니다.
- 주문 정보는 Django 서버로 전송되어 SQLite에 저장됩니다.
### 2. Order Processing
- 로봇은 Django 서버에 주기적으로 HTTP 요청을 보내 새 주문이 있는지 확인합니다.
- 주문이 접수되면 로봇은 커피 드립 과정을 시작합니다.
### 3. Coffee Brewing Process
- 커피 드립 과정은 린싱, 블루밍, 드립의 세 가지 단계로 이루어집니다.
- 린싱과 블루밍 단계에서는 인간의 개입이 필요하며, 이는 Yolov8 기반의 컴퓨터 비전 시스템을 통해 확인됩니다.
#### 3.1. Rinsing
- 로봇은 커피 드리퍼를 린싱하여 준비합니다.
- 인간 개입: 필터가 올바르게 놓였는지, 드리퍼가 제대로 위치했는지 확인합니다.
- 비전 체크: Yolov8이 드리퍼와 필터가 준비되었는지 확인합니다.
#### 3.2. Blooming
- 로봇은 커피 가루에 뜨거운 물을 부어 블루밍을 유도합니다.
- 인간 개입: 적절한 양의 커피 가루가 추가되었는지 확인합니다.
- 비전 체크: Yolov8이 커피 가루가 올바르게 놓였는지 확인합니다.
#### 3.3. Dripping
- 로봇은 드립 과정을 제어하여 커피를 추출합니다.
- 블루밍 완료 후 일정 시간이 지나면 드립을 시작합니다.
### 4. Completion
- 드립 과정이 완료되면 로봇이 주문 완료를 알립니다.
- Django 서버는 주문 상태를 업데이트하고, 안드로이드 앱은 사용자에게 이를 알립니다.
  
## Project Structure
- backend: Django 프로젝트 디렉토리로, API, 모델, 데이터베이스 설정을 포함합니다.
- robot: 로봇의 작동을 위한 스크립트가 포함되어 있으며, 주문 가져오기, 커피 드립 논리, 비전 체크 등이 포함됩니다.
- vision: Yolov8 기반의 컴퓨터 비전 스크립트 및 모델 설정이 포함됩니다.
- app: 안드로이드 앱 디렉토리로, 주문 및 시스템과 상호작용하는 사용자 인터페이스를 포함합니다.

## Installation
### Setup
```
pip install -r requirements.txt
```

## Contributors
이휘성, 김경태

## License
이 프로젝트는 Apache License 2.0에 따라 배포됩니다.
