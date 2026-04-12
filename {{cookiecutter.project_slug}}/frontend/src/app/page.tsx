import Image from "next/image";
import SignIn from "../components/auth/signin-button";
import { auth } from "@/auth";
import { signOut } from "@/auth";

type SessionData = Awaited<ReturnType<typeof auth>>;

function SignOut() {
  return (
    <div>
      <form
        action={async () => {
          "use server";
          await signOut();
        }}
      >
        <button type="submit">Sign out</button>
      </form>
    </div>
  );
}

function SessionInfo({ data }: { data: SessionData }) {
  if (!data) {
    return null;
  }

  const profile = data.profile as
    | {
        given_name?: string;
        family_name?: string;
        email?: string;
      }
    | undefined;
  const account = data.account as
    | {
        access_token?: string;
      }
    | undefined;

  const fullName = [profile?.given_name, profile?.family_name]
    .filter(Boolean)
    .join(" ");
  const greeting = fullName || data.user?.name || data.user?.email || "there";

  return (
    <div>
      <pre className="p-4 text-left bg-gray-100 dark:bg-neutral-800/30">
        Hello, {greeting}!
      </pre>
      <pre className="p-4 text-left bg-gray-100 dark:bg-neutral-800/30">
        ID: {data.user?.id ?? "Unavailable"}
      </pre>
      <pre className="p-4 text-left bg-gray-100 dark:bg-neutral-800/30">
        Email: {profile?.email ?? data.user?.email ?? "Unavailable"}
      </pre>
      <pre className="p-4 text-left bg-gray-100 dark:bg-neutral-800/30">
        Token: {account?.access_token ?? "Unavailable"}
      </pre>
    </div>
  );
}

function HandleSign({ data }: { data: SessionData }) {
  return data ? <SignOut /> : <SignIn />;
}

export default async function Home() {
  const session = await auth();

  return (
    <div className="grid min-h-screen grid-rows-[20px_1fr_20px] items-center justify-items-center gap-16 p-8 pb-20 font-(family-name:--font-geist-sans) sm:p-20">
      <main className="row-start-2 flex flex-col items-center gap-8 sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <h1 className="text-4xl font-bold text-center sm:text-left">
          Django Liberty 🗽
        </h1>
        <ol className="list-inside list-decimal text-center text-sm/6 font-(family-name:--font-geist-mono) sm:text-left">
          <li className="mb-2 tracking-[-.01em]">
            Get started by editing{" "}
            <code className="rounded bg-black/5 px-1 py-0.5 font-(family-name:--font-geist-mono) font-semibold dark:bg-white/6">
              app/page.tsx
            </code>
            .
          </li>
          <li className="tracking-[-.01em]">
            Save and see your changes instantly.
          </li>
        </ol>

        <SessionInfo data={session} />

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <div className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto">
            <HandleSign data={session} />
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={20}
              height={20}
            />
          </div>

          <a
            className="flex h-10 w-full items-center justify-center rounded-full border border-solid border-black/8 px-4 text-sm font-medium transition-colors hover:border-transparent hover:bg-[#f2f2f2] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] sm:h-12 sm:w-auto sm:px-5 sm:text-base md:w-[158px]"
            href={`${process.env.API_URL ?? "http://localhost:8000"}/account/signup`}
            target="_blank"
            rel="noopener noreferrer"
          >
            Sign Up
          </a>
        </div>
      </main>

      <footer className="row-start-3 flex flex-wrap items-center justify-center gap-6">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Examples
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Go to nextjs.org →
        </a>
      </footer>
    </div>
  );
}
