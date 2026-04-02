# n8n-mysql-docker
n8n으로 docker 사용해보기 

## 📋 프로젝트 개요

Docker 및 Docker Compose를 활용하여 n8n 워크플로우 자동화 툴과 MySQL 데이터베이스를 연동한 프로젝트입니다.

---

## 🛠️ 사용 기술

| 기술 | 버전 |
|------|------|
| Docker | 26.x |
| Docker Compose | v2.x |
| n8n | latest |
| MySQL | 8.0 |
| Ubuntu | 24.04 |

---

## 📁 프로젝트 구조

```
n8n-mysql-project/
├── docker-compose.yml   # 컨테이너 구성 파일
├── .env                 # 환경 변수 설정
└── README.md            # 프로젝트 설명
```

---

## ⚙️ 환경 변수 (.env)

```env
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=n8n_db
MYSQL_USER=n8n_user
MYSQL_PASSWORD=n8npassword
N8N_USER=admin
N8N_PASSWORD=adminpassword
```

---

## 🐳 docker-compose.yml 구성

### MySQL 서비스
- 이미지: `mysql:8.0`
- 포트: `3306:3306`
- 데이터 영속성: named volume (`mysql_data`)

### n8n 서비스
- 이미지: `n8nio/n8n`
- 포트: `5678:5678`
- MySQL DB 연동 설정
- 데이터 영속성: named volume (`n8n_data`)
- `depends_on: mysql` 으로 실행 순서 보장

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

### 3. n8n 접속
브라우저에서 접속:
```
http://[Ubuntu IP]:5678
```

| 항목 | 값 |
|------|------|
| ID | admin |
| Password | adminpassword |

---

## 🔄 n8n 워크플로우

### 워크플로우 구성
```
Manual Trigger → MySQL (CREATE TABLE) → MySQL (INSERT) → MySQL (SELECT)
```

### 실행 내용
1. **CREATE TABLE** - `test_table` 테이블 생성
```sql
CREATE TABLE IF NOT EXISTS test_table (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

2. **INSERT** - 데이터 삽입
```sql
INSERT INTO test_table (name) VALUES ('Docker n8n Test');
```

3. **SELECT** - 데이터 조회
```sql
SELECT * FROM test_table;
```

---

## 🌐 네트워크 구성

- 브릿지 네트워크 `n8n-network` 사용
- n8n → MySQL 컨테이너 이름(`mysql`)으로 내부 통신

---

## 📌 개발 환경

- **Host OS**: Windows
- **VM**: VMware Workstation
- **Guest OS**: Ubuntu 24.04
- **IDE**: VSCode (Remote-SSH 원격 접속)

---

## 👤 개발자

- GitHub: [ChoiYunSik02](https://github.com/ChoiYunSik02)
