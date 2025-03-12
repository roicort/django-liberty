# Description: Dockerfile for Nuxt app

FROM node:22

WORKDIR /app

RUN npm install -g pnpm

COPY src .

RUN pnpm install

EXPOSE 3000

CMD ["pnpm", "run", "dev", "-o", "--host"]
