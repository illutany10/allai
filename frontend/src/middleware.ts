export { auth as middleware } from "@/auth"

export const config = {
  matcher: [
    // 보호할 경로들을 명시적으로 지정 (로그인 페이지와 API 경로 제외)
    "/((?!api|_next/static|_next/image|favicon.ico|login).*)",
  ],
}