"""
Supabase 클라이언트 설정 및 헬퍼 함수들
Django와 Supabase를 연동하기 위한 유틸리티
"""
import os
from supabase import create_client, Client
from django.conf import settings

def get_supabase_client() -> Client:
    """
    Supabase 클라이언트 인스턴스를 반환합니다.
    """
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_ANON_KEY
    
    if not url or not key:
        raise ValueError(
            "SUPABASE_URL과 SUPABASE_ANON_KEY가 settings에 설정되어야 합니다."
        )
    
    return create_client(url, key)

def get_supabase_service_client() -> Client:
    """
    서비스 역할 키를 사용하는 Supabase 클라이언트를 반환합니다.
    관리자 권한이 필요한 작업에 사용됩니다.
    """
    url = settings.SUPABASE_URL
    service_key = settings.SUPABASE_SERVICE_ROLE_KEY
    
    if not url or not service_key:
        raise ValueError(
            "SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY가 settings에 설정되어야 합니다."
        )
    
    return create_client(url, service_key)

# 전역 클라이언트 인스턴스 (선택사항)
try:
    supabase: Client = get_supabase_client()
except (ValueError, AttributeError):
    # 설정이 없는 경우 None으로 설정
    supabase = None
