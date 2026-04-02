# n8n-mysql-docker
n8n으로 docker 사용해보기 

# 🪙 실시간 코인 가격 모니터링 시스템

## 📋 프로젝트 개요

Docker 및 Docker Compose를 활용하여 Binance API에서 실시간 코인 가격을 수집하고,
n8n 워크플로우로 자동화하여 MySQL에 저장 후 Grafana 대시보드로 시각화하는 시스템입니다.

---

## 🛠️ 사용 기술

| 기술 | 버전 | 역할 |
|------|------|------|
| Docker | 26.x | 컨테이너 실행 환경 |
| Docker Compose | v2.x | 멀티 컨테이너 관리 |
| n8n | latest | 데이터 수집 자동화 |
| MySQL | 8.0 | 데이터 저장 |
| Grafana | latest | 실시간 데이터 시각화 |
| Binance API | - | 코인 가격 데이터 제공 |
| Ubuntu | 24.04 | 운영체제 |

---

## 📁 프로젝트 구조

```
coin-monitor/
├── docker-compose.yml   # 컨테이너 구성 파일
├── .env                 # 환경 변수 설정
└── README.md            # 프로젝트 설명
```

---

## ⚙️ 환경 변수 (.env)

```env
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=coin_db
MYSQL_USER=coin_user
MYSQL_PASSWORD=coinpassword
N8N_USER=admin
N8N_PASSWORD=adminpassword
```

---

## 🐳 docker-compose.yml 구성

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - coin-network

  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=mysqldb
      - DB_MYSQLDB_HOST=mysql
      - DB_MYSQLDB_PORT=3306
      - DB_MYSQLDB_DATABASE=${MYSQL_DATABASE}
      - DB_MYSQLDB_USER=${MYSQL_USER}
      - DB_MYSQLDB_PASSWORD=${MYSQL_PASSWORD}
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_SECURE_COOKIE=false
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - mysql
    networks:
      - coin-network

  grafana:
    image: grafana/grafana
    container_name: grafana
    restart: always
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - mysql
    networks:
      - coin-network

volumes:
  mysql_data:
  n8n_data:
  grafana_data:

networks:
  coin-network:
    driver: bridge
```

---

## 🔄 n8n 워크플로우 구성

### 워크플로우 흐름
```
Schedule Trigger (10초마다)
        ↓
HTTP Request (Binance API 호출)
        ↓
Code 노드 (데이터 변환)
        ↓
MySQL (테이블 생성)
        ↓
MySQL (데이터 삽입)
        ↓
MySQL (데이터 조회)
```

### Binance API URL
```
https://api.binance.com/api/v3/ticker/price?symbols=["BTCUSDT","ETHUSDT"]
```

### 수집 데이터
```json
[
  { "symbol": "BTCUSDT", "price": "66866.38" },
  { "symbol": "ETHUSDT", "price": "2055.02" }
]
```

### MySQL 테이블 구조
```sql
CREATE TABLE IF NOT EXISTS coin_prices (
  id INT AUTO_INCREMENT PRIMARY KEY,
  symbol VARCHAR(20),
  price DECIMAL(20, 8),
  collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 데이터 삽입 쿼리
```sql
INSERT INTO coin_prices (symbol, price)
VALUES ('{{ $json.symbol }}', {{ $json.price }});
```

---

## 📊 Grafana 대시보드 구성

### MySQL 데이터 소스 설정
| 항목 | 값 |
|------|------|
| Host | `mysql:3306` |
| Database | `coin_db` |
| User | `coin_user` |
| Password | `coinpassword` |

### BTC 가격 그래프 쿼리
```sql
SELECT
  collected_at AS time,
  price AS value,
  symbol AS metric
FROM coin_prices
WHERE symbol = 'BTCUSDT'
AND collected_at >= NOW() - INTERVAL 5 MINUTE
ORDER BY collected_at ASC
```

### ETH 가격 그래프 쿼리
```sql
SELECT
  collected_at AS time,
  price AS value,
  symbol AS metric
FROM coin_prices
WHERE symbol = 'ETHUSDT'
AND collected_at >= NOW() - INTERVAL 5 MINUTE
ORDER BY collected_at ASC
```

---

## 🚀 실행 방법

### 1. 컨테이너 실행
```bash
docker compose up -d
```

### 2. 실행 상태 확인
```bash
docker compose ps
```

### 3. 서비스 접속

| 서비스 | 주소 | ID | PW |
|------|------|------|------|
| n8n | `http://[IP]:5678` | admin | adminpassword |
| Grafana | `http://[IP]:3000` | admin | admin |

---

## 🌐 네트워크 구성

- 브릿지 네트워크 `coin-network` 사용
- n8n → MySQL 컨테이너 이름으로 내부 통신
- Grafana → MySQL 컨테이너 이름으로 내부 통신

---

## 📌 개발 환경

- **Host OS**: Windows
- **VM**: VMware Workstation
- **Guest OS**: Ubuntu 24.04
- **IDE**: VSCode (Remote-SSH 원격 접속)

---

## 👤 개발자

- GitHub: [ChoiYunSik02](https://github.com/ChoiYunSik02)

