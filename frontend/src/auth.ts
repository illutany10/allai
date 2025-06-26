import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) {
          return null;
        }

        try {
          const res = await fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/auth/login/`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                username: credentials.username,
                password: credentials.password,
              }),
            }
          );

          if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.error || "Invalid credentials");
          }

          const data = await res.json();
          const user = {
            ...data.user,
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
          };

          return user;
        } catch (e: any) {
          throw new Error(e.message);
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken;
        token.refreshToken = user.refreshToken;
        token.user = user;
      }
      return token;
    },
    async session({ session, token }) {
      session.user = token.user as any;
      session.accessToken = token.accessToken as string;
      session.refreshToken = token.refreshToken as string;
      return session;
    },
    authorized: ({ auth, request: { nextUrl } }) => {
      const isLoggedIn = !!auth?.user;
      const isOnLogin = nextUrl.pathname.startsWith("/login");

      // 로그인 페이지에서는 이미 로그인된 유저를 홈으로 리다이렉트
      if (isOnLogin && isLoggedIn) {
        return Response.redirect(new URL("/", nextUrl));
      }

      // 로그인이 필요한 페이지에서는 로그인 여부 확인
      return isLoggedIn;
    },
  },
  pages: {
    signIn: "/login",
  },
});