# Next.js + Django + Supabase 프로젝트

Django 백엔드와 Next.js 프론트엔드, 그리고 Supabase 데이터베이스를 사용하는 풀스택 프로젝트입니다.

## 🚀 시작하기

### 1. Supabase 프로젝트 설정

1. [Supabase](https://supabase.com)에 가입하고 새 프로젝트를 생성하세요
2. 프로젝트 대시보드에서 **Settings > Database**로 이동
3. **Connection String** 섹션에서 데이터베이스 연결 정보를 확인하세요

### 2. 환경 변수 설정

`backend/.env.example`을 복사하여 `backend/.env` 파일을 생성하고 Supabase 정보를 입력하세요:

```bash
cp backend/.env.example backend/.env
```

**Supabase에서 가져올 정보:**
- **DB_HOST**: `db.xxx.supabase.co` 형식
- **DB_PASSWORD**: 프로젝트 생성 시 설정한 비밀번호
- **SUPABASE_URL**: `https://xxx.supabase.co`
- **SUPABASE_ANON_KEY**: API Keys에서 확인

### 3. Python 패키지 설치

```bash
cd backend
pip3 install -r requirements.txt
```

### 4. 데이터베이스 마이그레이션

```bash
python3 manage.py migrate
```

### 5. Django 서버 실행

```bash
python3 manage.py runserver
```

### 6. Next.js 프론트엔드 실행 (별도 터미널)

```bash
cd frontend
npm install
npm run dev
```

## 📋 주요 기능

- ✅ Django REST Framework 백엔드
- ✅ Supabase PostgreSQL 데이터베이스
- ✅ Next.js TypeScript 프론트엔드
- ✅ 환경 변수 관리
- ✅ SSL 보안 연결

## 🔧 개발 도구

- **Backend**: Django 5.2.3, Python 3.13
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **환경 관리**: python-dotenv

## 📚 Supabase 사용법

### 인증 설정
Supabase 대시보드에서 **Authentication > Settings**에서 인증 제공자를 설정할 수 있습니다.

### 실시간 기능
Supabase의 실시간 기능을 사용하려면 프론트엔드에서 Supabase 클라이언트를 설정하세요.

### API 자동 생성
Supabase는 데이터베이스 스키마를 기반으로 RESTful API를 자동 생성합니다.

## 🤝 기여하기

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
